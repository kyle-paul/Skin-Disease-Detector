[toc]
## **Problems** 

## **How AI with computer vision can solve**

## **Training process**

### **Data gathering**
#### **The difficulty in the field of automated diagnosis of pigmented skin lesions**
- Training of neural networks for automated diagnosis of pigmented skin lesions is hampered by the small size and lack of diversity of available datasets of dermatoscopic images
- Building a classifier for multiple diseases is more challenging than binary classification. Currently, reliable multi-class predictions are only available for clinical images of skin diseases but not for dermatoscopic images.
- With the HAM10000 dataset below and my transfer-learning model, I hope that I can overcome thoses obstacles so that it could serve as benchmark set for the comparisons of humans and machines

|  | | 
| -------- | -------- | 
| Design Type(s)    | database creation objective • data integration objective • image format conversion objective  | 
|Measurement Type(s)| skin lesions |
|Technology Type(s)|digital curation|
|Factor Type(s)|diagnosis • Diagnostic Procedure • age • biological sex • animal body part|
|Sample Characteristic(s)|Homo sapiens • skin of body|

#### **Dataset preparation**
- The HAM10000 dataset is a large collection of multi-source dermatoscopic images of common pigmented skin lesions. More than 50% of lesions have been **confirmed** by pathology, while the ground truth for the rest of the cases was either follow-up, expert consensus, or confirmation by in-vivo confocal microscopy.
- **Schematic flow of dataset workup methods**: Image and data content from different sources were entered into a pipeline to organize and clean data, with final images being standardized and stored in a common format.
<br>

![data_gather](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/81d76a22-7b63-4e7a-a1bf-8370d0415287)


#### **7 most dangerous skin disease categories:**

| Categories | Description |
| -------- | -------- |
| **akiec**  ![Hk5REdhYh](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/63666c43-47d0-47d5-b006-e055367181dc)| Actinic keratoses and Bowen’s disease are non-invasive forms of skin cancer that can be treated without surgery. they can either progress to invasive squamous cell carcinom or not. They are usually caused by sun damage and have no pigment, but some cases may be pigmented or caused by a virus. They can become invasive if not treated.|
|**bcc**![S1QDSO2t2](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/0c4a333e-43ff-44ed-815a-c42d2c7426ff)|Basal cell carcinoma is a common variant of epithelial skin cancer that rarely metastasizes but grows destructively if untreated. It appears in different morphologic variants (flat, nodular, pigmented, cystic),|
|**bkl** ![BkvqBOhtn](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/9a386d4c-62d2-418d-8028-e6753a6e4e83)| Benign keratosis is a term for harmless skin growths that are related to sun damage or aging. They can look different depending on where they are and what type they are. Some of them can look like skin cancer but are not.|
|**df**![Hk7hBuhKn](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/15c78699-3a80-4ae3-ac7b-3289e4210ef4)|Dermatofibroma is a benign skin lesion regarded as either a benign proliferation or an inflammatory reaction to minimal trauma. The most common dermatoscopic presentation is reticular lines at the periphery with a central white patch denoting fibrosis|
|**nv**![Bk5pHdnF3](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/fd2f10f6-cc0a-4362-804b-4b4ba4ba95b6)|Melanocytic nevi are benign neoplasms of melanocytes and appear in a myriad of variants. The variants may differ significantly from a dermatoscopic point of view. In contrast to melanoma they are usually symmetric with regard to the distribution of color and structure|
|**mel**![HJ-kUu3Fh](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/d7e4ebcc-0003-4779-b5dc-03c3bdf7ce48)|Melanoma is a malignant neoplasm derived from melanocytes that may appear in different variants. If excised in an early stage it can be cured by simple surgical excision. Melanomas can be invasive or noninvasive. Melanomas are usually, albeit not always, chaotic, and some melanoma specific criteria depend on anatomic site.|
|**vasc** ![By1e8u3Kh](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/2218986e-06a0-4e65-afaa-f5d3a161093e)|Vascular skin lesions in the dataset range from cherry angiomas to angiokeratomas31 and pyogenic granulomas. Hemorrhage is also included in this category. Angiomas are dermatoscopically characterized by red or purple color and solid, well circumscribed structures known as red clods or lacunes.|

![H1pg1Ont2](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/75174552-d1fa-4280-ba74-cda521daae79)

### **Data Exploration**
[Read Harvard article](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T) 
[The final dataset](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000) consists of 10015 dermatoscopic images stored in two folders `HAM10000_images_part_1` and `HAM10000_images_part_2` with a csv file `HAM10000_metadata.csv` to manage the `lession_id` `image_id` `dx`(labels) `dx_type` `age` `sex` `localization`.
- This dataset is unbalanced because it is **biased** towards melanocytic lesions. However, I have already resample the dataset in my jupyter notebook to remove the consequence of bias in the dataset.
![rkk9_unFh](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/5b800cb0-833d-4462-ae9a-3271336d8960)
- The below graph show the distribution of 7 skin diseases across different body parts:
    - The most common body part affected by these skin diseases is the scalp, followed by the face and the lower extremity.
    - The least common body part affected by these skin diseases is the neck, followed by the genital and the unknown.
    - The chest, trunk, and upper extremity have similar counts of around 500 each.
![image](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/8a5fd590-9e26-4e61-a6c8-80fe5fa48ef6)
- The next bar graph shows the distribution of sex among the patients with skin diseases:
    - The majority of the patients are male, followed by female and then unknown.
    - The difference between male and female patients is not very large, but the difference between known and unknown sex is significant.
![image](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/f3010c92-d7a7-47a1-a5b4-364a0c76c589)

### **Data processing**

- I divided our dataset into two folders: `train` and `test`, which are in the `output` folder. Each of these folders has seven subfolders for the classes/labels.
- And there is a folder called `reorganized` storing 7 subfolders for classes/labels: `akiec`, `bcc`, `bkl`, `df`, `mel`, `nv`, `vasc`.
- When using transfer learning, I also add augmentation techniques (`RandomFlip`, `RandomRotation`)

### Training model
#### **Transfer learning with Mobilenet_v2**

| The model base architecture: | 
| -------- | 
| ![Syw81t3Fn](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/95c51fd8-3f3e-4754-b286-eb917e78b564) | 


| The fine-tuned model with 100 layers unfreezed/trainable | 
| -------- | 
| ![ryuu1Y3K2](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/d71b2a2b-6abb-4848-913f-531fbd5b901c) | 


#### **Train from scratch**

| The model architecture | 
| -------- | 
| ![CNN0 h5](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/1d414c01-48ad-4905-9cd5-5bb397c0f51f)| 

### **Metrics**

| Before fine-tuning | After fine-tuning |
| -------- | -------- | 
| ![image](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/5046bed2-a847-4ec5-aba4-129c22dee684) | ![image](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/9caad979-c5d2-4463-a42d-6714aa4eadd8)
| 


| CNN0 accuracy | CNN0 loss |
| -------- | -------- | 
| ![image](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/1affd86e-f789-4ff4-bbb6-9c38deac6080)| ![image](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/f2327e60-a014-4f2c-ab29-fbff082a7356)
|


## **Website**
### **Demo** 

### **How to use the code**
First you need to clone this repository to your local system. Open terminal and then paste this command line
```
git clone https://github.com/kyle-paul/Skin-Disease-Detector.git
```
Next move into the cloned directory
```
cd Skin-Disease-Detector
```
Type this to open your default code editor. As usual, it will open vscode if you use vscode as your default code editor
```
. code
```
Create a virtual environment with venv to avoid conflicts in library versions and modules
```
python -m venv .venv
```
Activate the environment
```
.\.venv\Scripts\activate
```
Install all neccessary libraries with a specific version
```
pip install -r requirements.txt
```
Now if you want to view all libraries and modules in your virtual environment, paste this command line
```
pip freeze
```
To run the server backend flask python, run this line of command
```
flask --debug run
```
Now, the website should be available at the port `127.0.0.1:5000`



### **Appendix**
- **Dermatoscopic** is an adjective that describes something related to dermatoscopy, which is the examination of skin lesions with a dermatoscope. A dermatoscope is a hand-held device that uses light and magnification to show extra details of the skin, hair, or nails that are not visible to the naked eye. Dermatoscopy can help diagnose certain skin conditions, such as melanoma, by revealing specific patterns and features of pigmented skin lesions.
