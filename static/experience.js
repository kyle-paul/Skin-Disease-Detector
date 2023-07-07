const status = document.getElementById('status');
if (status) {
    status.innerText = 'Loaded TensorFlow.js - version: ' + tf.version.tfjs;
}


const STATUS = document.getElementById('status');
const VIDEO = document.getElementById('webcam');
const ENABLE_CAM_BUTTON = document.getElementById('enableCam');
const RESET_BUTTON = document.getElementById('reset');
const TRAIN_BUTTON = document.getElementById('train');
const MOBILE_NET_INPUT_WIDTH = 224;
const MOBILE_NET_INPUT_HEIGHT = 224;
const STOP_DATA_GATHER = -1;
const CLASS_NAMES = [];

ENABLE_CAM_BUTTON.addEventListener('click', enableCam);
TRAIN_BUTTON.addEventListener('click', trainAndPredict);
RESET_BUTTON.addEventListener('click', reset);

const buttonAnimate = document.querySelectorAll('button.animate');
for (let i = 0; i < buttonAnimate.length; i++) {
    buttonAnimate[i].addEventListener('click', (e) => {
        e.preventDefault;
        buttonAnimate[i].classList.add('animate');
        setTimeout(() => {
            buttonAnimate[i].classList.remove('animate');
        }, 600);
    });
}

let dataCollectorButtons = document.querySelectorAll('button.dataCollector');
for (let i = 0; i < dataCollectorButtons.length; i++) {
    dataCollectorButtons[i].addEventListener('mousedown', gatherDataForClass);
    dataCollectorButtons[i].addEventListener('mouseup', gatherDataForClass);
    // Populate the human readable names for classes
    CLASS_NAMES.push(dataCollectorButtons[i].getAttribute('data-name'));
}

let mobilenet = undefined;
let gatherDataState = STOP_DATA_GATHER;
let videoPlaying = false;
let trainingDataInputs = [];
let trainingDataOutputs = [];
let examplesCount = [];
let predict = false;

// Load the Mobilenet model
async function loadMobileNetFeatureModel() {
    const URL = 'https://tfhub.dev/google/tfjs-model/imagenet/mobilenet_v3_small_100_224/feature_vector/5/default/1';
    mobilenet = await tf.loadGraphModel(URL, { fromTFHub: true });
    STATUS.innerText = "Mobile v3 loaded successfully";

    // Warm up the model by passing zeros through it once
    tf.tidy(function () {
        let answer = mobilenet.predict(tf.zeros([1, MOBILE_NET_INPUT_HEIGHT, MOBILE_NET_INPUT_WIDTH, 3]));
        console.log(answer.shape);
    });
}

loadMobileNetFeatureModel();

// Create and compile the model
let model = tf.sequential();
model.add(tf.layers.dense({ inputShape: [1024], units: 128, activation: 'relu' }));
model.add(tf.layers.dense({ units: CLASS_NAMES.length, activation: 'softmax' }));
model.summary();

model.compile({
    optimizer: 'adam',
    loss: (CLASS_NAMES.length === 2) ? 'binaryCrossentropy' : 'categoricalCrossentropy',
    metrics: ['accuracy']
});

// Check browser can get user media
function hasGetUserMedia() {
    return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}


// add supporting function
function enableCam() {
    if (hasGetUserMedia) {
        // get user media parameters
        const constraints = {
            video: true,
            width: 640,
            height: 480,
        };
        // Activate the webcam stream
        navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
            VIDEO.srcObject = stream;
            VIDEO.addEventListener('loadeddata', function () {
                videoPlaying = true;
                // ENABLE_CAM_BUTTON.classList.add('removed');
            });
        });
    } else {
        console.warn('No user media')
    }
}

function gatherDataForClass() {
    let classNumber = parseInt(this.getAttribute('data-1hot')); // get attribute is a string and then cast into an integer
    gatherDataState = (gatherDataState == STOP_DATA_GATHER) ? classNumber : STOP_DATA_GATHER;
    dataGatherLoop();
}

function dataGatherLoop() {
    if (videoPlaying && gatherDataState !== STOP_DATA_GATHER) {
        let imageFeatures = tf.tidy(function () {
            let videoFrameAsTensor = tf.browser.fromPixels(VIDEO);
            let resizedTensorFrame = tf.image.resizeBilinear(videoFrameAsTensor, [MOBILE_NET_INPUT_HEIGHT, MOBILE_NET_INPUT_WIDTH], true);
            let normalizedTensorFrame = resizedTensorFrame.div(255);
            return mobilenet.predict(normalizedTensorFrame.expandDims()).squeeze();
        });

        trainingDataInputs.push(imageFeatures);
        trainingDataOutputs.push(gatherDataState);

        // Initialize array index element if currently undefined
        if (examplesCount[gatherDataState] === undefined) {
            examplesCount[gatherDataState] = 0;
        }
        examplesCount[gatherDataState]++;

        STATUS.innerHTML = '';
        for (let n = 0; n < CLASS_NAMES.length; n++) {
            STATUS.innerHTML += CLASS_NAMES[n] + ' - Data Count: ' + examplesCount[n] + '   ';
        }
        window.requestAnimationFrame(dataGatherLoop);
    }
}


async function trainAndPredict() {
    predict = false;
    tf.util.shuffleCombo(trainingDataInputs, trainingDataOutputs);
    let outputAsTensor = tf.tensor1d(trainingDataOutputs, 'int32');
    let oneHotOutputs = tf.oneHot(outputAsTensor, CLASS_NAMES.length);
    let inputAsTensor = tf.stack(trainingDataInputs);

    let results = await model.fit(inputAsTensor, oneHotOutputs, {
        shuffle: true,
        batchSize: 5,
        epochs: 10,
        callbacks: { onEpochEnd: logProgress }
    });

    outputAsTensor.dispose();
    inputAsTensor.dispose();
    oneHotOutputs.dispose();
    predict = true;
    predictLoop();
}

function logProgress(epoch, logs) {
    console.log('Data for epoch: ' + epoch, logs);
}

var progress = document.getElementById("progress");
var finished = false;
function showOrHideProgress() {
    if (finished) {
        progress.style.visibility = "visible";
    } else {
        progress.style.visibility = "hidden";
    }
}

function predictLoop() {
    if (predict) {
        tf.tidy(function () {
            let videoFrameAsTensor = tf.browser.fromPixels(VIDEO).div(255);
            let resizedTensorFrame = tf.image.resizeBilinear(videoFrameAsTensor, [MOBILE_NET_INPUT_HEIGHT, MOBILE_NET_INPUT_WIDTH], true);
            let imageFeatures = mobilenet.predict(resizedTensorFrame.expandDims());
            let prediction = model.predict(imageFeatures).squeeze();
            let highestIndex = prediction.argMax().arraySync();
            let predictionArray = prediction.arraySync();

            STATUS.innerHTML = "Prediction: " + CLASS_NAMES[highestIndex] + ' with ' + Math.floor(predictionArray[highestIndex] * 100) + '% confidence';
        });

        window.requestAnimationFrame(predictLoop);
    }
}

function reset() {
    predict = false;
    examplesCount.splice(0);
    for (let i = 0; i < trainingDataInputs.length; i++) {
        trainingDataInputs[i].dispose();
    }
    trainingDataInputs.splice(0);
    trainingDataOutputs.splice(0);
    STATUS.innerHTML = "No data collected";
    console.log('Tensor in memory: ' + tf.memory().numTensors);
}