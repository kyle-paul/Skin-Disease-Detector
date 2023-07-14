# Skin Diseases Detector (Using Machine Learning and Telehealth to Detect and Treat Skin Diseases)

## **Project Description** 
Skin diseases are conditions that affect your skin and may cause rashes, inflammation, itchiness or other skin changes. Some skin diseases are minor, while others can be serious and even life-threatening. One of the major complications of some skin diseases is the increased risk of skin cancer, which is the uncontrolled growth of abnormal skin cells. Skin cancer can be caused by various factors, such as sun exposure, genetics, or infections.

Many regions in the world have limited access to healthcare services, which makes it difficult for people to get timely and accurate diagnosis and treatment for their skin problems. This can lead to worsening of their condition, lower quality of life, and higher mortality rates.

To address this issue, I have created a web application that uses machine learning to detect and classify seven of the most common and dangerous skin diseases: Actinic keratoses(akeic), Basal cell carcinoma(bcc), Benign keratosis (bkl), Dermatofibroma (df), Melanocytic nevi (nv), and Vascular (vasc). The web application allows users to upload a picture of their skin lesion and get a provisional diagnosis from the AI model. The provisional diagnosis is not a substitute for a professional medical opinion, but rather a guidance tool that can help users understand their condition better and seek appropriate care.

The web application also provides a telehealth service that connects users with doctors on my website who can review the provisional diagnosis from the AI model and give an accurate prescription. This way, users can get access to quality healthcare from anywhere in the world, without having to travel long distances or wait for appointments. The telehealth service also helps reduce the burden on the healthcare system and improve the efficiency and effectiveness of care delivery.

My web application aims to empower people with skin diseases by providing them with information, education, and support. I hope that my web application can make a positive difference in the lives of millions of people who suffer from skin diseases and improve their health outcomes.

## **Website application**
### **Video Demo** 
<iframe width="560" height="315" src="https://www.youtube.com/embed/HY2TxxKwybI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

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

#### Comparsion about symtomps, complications, and treatment (should be read by website users)
| Skin disease | Description | Symptoms | Treatment | Complications |
| --- | --- | --- | --- | --- |
| Actinic keratosis | A precancerous skin condition caused by sun damage. It affects about 10% of adults in the United States¹. | A thick, scaly or crusty patch of skin that is usually less than 2 cm in diameter. It often appears on sun-exposed areas such as the face, scalp, arms and hands. It may be pink, brown, tan or gray in color². | Topical creams or gels, cryotherapy (freezing), photodynamic therapy (light and drug), chemical peels or surgery². | About 10% of actinic keratoses may progress to squamous cell carcinoma, a type of skin cancer that can spread to other organs². |
| Basal cell carcinoma | The most common type of skin cancer. It affects about 3 million people in the United States each year³. It rarely metastasizes (spreads to other organs) but can be locally destructive⁴. | A shiny, pearly or translucent bump or nodule that may bleed or crust over. It may also appear as a flat, scaly or red patch or a scar-like area. It usually occurs on sun-exposed areas such as the face, ears and neck⁴. | Surgery, electrodessication and curettage (scraping and burning), radiation therapy, topical creams or gels or oral medications⁴. | Recurrence, disfigurement, nerve damage or eye problems if left untreated or if located near vital structures⁴. |
| Benign keratosis | A general term for noncancerous growths on the skin. They include seborrheic keratoses, cherry angiomas and skin tags. They are very common and harmless but may be cosmetically bothersome⁵. | Vary depending on the type of keratosis. Seborrheic keratoses are brown, black or tan waxy bumps that look like they are stuck on the skin. Cherry angiomas are small red spots caused by dilated blood vessels. Skin tags are soft, flesh-colored growths that hang from the skin by a thin stalk⁵. | No treatment is necessary unless they are irritated, inflamed or bleeding. They can be removed by cryotherapy (freezing), electrodessication and curettage (scraping and burning), laser therapy or surgery⁵. | Rarely, they may become infected or inflamed. They may also be mistaken for malignant lesions⁵. |
| Dermatofibroma | A benign fibrous nodule that develops in the dermis (the middle layer of the skin). It affects about 1% of adults and is more common in women than men⁶. The cause is unknown but may be related to trauma or insect bites. | A firm, raised, round or oval bump that is usually less than 1 cm in diameter. It may be pink, brown, gray or black in color. It usually occurs on the lower legs but can appear anywhere on the body. It may be tender or itchy. | No treatment is necessary unless it causes symptoms or cosmetic concerns. It can be removed by surgery or cryotherapy (freezing). | Rarely, it may become infected or ulcerated. It may also be mistaken for malignant lesions. |
| Melanoma | The most serious type of skin cancer. It affects about 100,000 people in the United States each year and accounts for about 75% of all skin cancer deaths. It develops from melanocytes (the cells that produce pigment) and can spread to other organs if not detected early. | A new or changing mole that has an irregular shape, uneven color, large size (>6 mm), blurred border or evolving appearance. It may also bleed, itch or ulcerate. It can occur anywhere on the body but is more common on sun-exposed areas such as the back, legs and arms. | Surgery, sentinel lymph node biopsy, immunotherapy, targeted therapy, chemotherapy or radiation therapy depending on the stage and location of the tumor. | Recurrence, metastasis (spread to other organs), lymphedema (swelling of the limbs due to lymph node removal), nerve damage or immune-related side effects from treatment. |
| Melanocytic nevi | Commonly known as moles. They are benign growths of melanocytes (the cells that produce pigment) on the skin. They affect almost everyone and are usually present at birth or develop during childhood or adolescence. | A small, round or oval spot that is usually brown, black or tan in color. It may be flat or raised, smooth or rough, hairy or hairless. It usually occurs on sun-exposed areas such as the face, arms and legs but can appear anywhere on the body. | No treatment is necessary unless they are suspicious for melanoma or cause cosmetic concerns. They can be removed by surgery, electrodessication and curettage (scraping and burning) or laser therapy. | Rarely, they may become dysplastic (abnormal) or malignant (cancerous). They may also be mistaken for malignant lesions. |
| Vascular lesions | A general term for abnormal blood vessels on the skin. They include port wine stains, hemangiomas and spider veins. They are usually congenital (present at birth) or develop during childhood. | Vary depending on the type of vascular lesion. Port wine stains are flat, red or purple patches that usually affect the face or neck. Hemangiomas are bright red, raised, soft and spongy growths that usually appear on the head or neck. Spider veins are thin, red or blue lines that branch out like a spider web on the legs or face. | No treatment is necessary unless they cause symptoms or cosmetic concerns. They can be treated by laser therapy, sclerotherapy (injection of a solution that shrinks the blood vessels), surgery or oral medications. | Rarely, they may bleed, ulcerate, become infected or interfere with vital functions such as vision, breathing or eating. |

### **Data Exploration**
[Read Harvard article](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T) 
[The final dataset](https://drive.google.com/drive/folders/1TrDSH-4agskvCawHsqwm6j29GQlmXjU7) consists of 10015 dermatoscopic images stored in two folders `HAM10000_images_part_1` and `HAM10000_images_part_2` with a csv file `HAM10000_metadata.csv` to manage the `lession_id` `image_id` `dx`(labels) `dx_type` `age` `sex` `localization`.
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

MobileNetV2 is a neural network architecture that is designed for efficient image classification on mobile devices. It is based on an inverted residual structure, where the input and output of each block are thin bottleneck layers, and the intermediate layer is expanded with depthwise convolutions. This reduces the computational cost and the number of parameters, while preserving the representational power of the network. MobileNetV2 also uses linear bottlenecks, which means that the last layer of each block does not have a non-linearity, to avoid information loss. MobileNetV2 can achieve state-of-the-art performance on multiple tasks and benchmarks, as well as across different model sizes.

| The model base architecture: | 
| -------- | 
| ![Syw81t3Fn](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/95c51fd8-3f3e-4754-b286-eb917e78b564) | 


| The fine-tuned model with 100 layers unfreezed/trainable | 
| -------- | 
| ![ryuu1Y3K2](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/d71b2a2b-6abb-4848-913f-531fbd5b901c) | 
| ![transfer](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/b256ecbc-2a16-4d75-ae2c-52f08d208873)|


#### **Train from scratch**

| The model architecture | | 
| -------- | --------| 
| ![cnn architecture from scratch](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/7cc51bcf-a140-4b58-95ea-7cf74b3bf94e) |![image](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/78b5c973-bba6-417a-b889-1bb05197710a)| 

### **Metrics**

| Before fine-tuning | After fine-tuning |
| -------- | -------- | 
| ![image](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/5046bed2-a847-4ec5-aba4-129c22dee684) | ![image](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/9caad979-c5d2-4463-a42d-6714aa4eadd8)| 

The model is learning well from the data and has low error on both training and validation datasets. The learning curves of a well-fit model show high performance and a small gap between the training and validation datasets.

| CNN0 accuracy | CNN0 loss |
| -------- | -------- | 
| ![image](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/39c06426-9d9f-4e74-b756-78d1cb91fbc7)| ![image](https://github.com/kyle-paul/Skin-Disease-Detector/assets/117391498/1aba4a4d-e099-4271-99f2-d44dc6dd1a67)|
