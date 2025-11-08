# Intelligent console Volcano dual-stream speech synthesis + tone cloning configuration tutorial

This tutorial is divided into 4 stages: preparation stage, configuration stage, cloning stage, and usage stage. It mainly introduces the process of configuring the Volcano dual-stream speech synthesis + tone cloning through the intelligent console.

## The first stage: preparation stage
The super administrator first activates the Volcano Engine service in advance and obtains the App ID and Access Token. By default, Huoshang Engine will give away a sound resource. This sound resource needs to be copied to this project.

If you want to clone multiple timbres, you need to purchase and activate multiple timbre resources. Just copy the sound ID (S_xxxxx) of each sound resource to this project. Then use the account assigned to the system. Here are the detailed steps:

### 1. Activate the volcano engine service
Visit https://console.volcengine.com/speech/app, create an application in the application management, and check the speech synthesis model and the sound reproduction model.

### 2. Get the timbre resource ID
Visit https://console.volcengine.com/speech/service/9999 and copy three items, namely App Id, Access Token and Sound ID (S_xxxxx). As shown in the picture

![Get sound resources](images/image-clone-integration-01.png)

## Phase 2: Configure the Volcano Engine Service

### 1. Fill in the volcano engine configuration

Use the super administrator account to log in to the intelligent console, click [Model Configuration] at the top, then click [Speech Synthesis] on the left side of the model configuration page, search for "Volcano Dual-Stream Speech Synthesis", click Modify, fill in the `App Id' of your Volcano engine into the [Application ID] field, and fill in the `Access Token` into the [Access Token] field. Then save.

### 2. Assign the timbre resource ID to the system account

Log in to the smart console with a super administrator account and click [Tone Clone] and [Tone Resources] at the top.

Click the Add button and select "Volcano Dual-Stream Speech Synthesis" in [Platform Name];

Fill in the sound resource ID (S_xxxxx) of your volcano engine in [Sound Resource ID], fill in and press Enter;

In [Attribution Account], select the system account you want to assign to. You can assign it to yourself. Then click save

## The third stage: cloning stage

If after logging in, click [Tone Clone] and [Tone Clone] at the top, and it displays [Your account currently has no tone resources, please contact the administrator to allocate tone resources], it means that you have not assigned the tone resource ID to this account in the second stage. That is to return to the second stage and allocate timbre resources to the corresponding accounts.

If you log in, click [Tone Clone] and [Tone Clone] at the top to see the corresponding tone list. Please continue.

You will see the corresponding tone list in the list. Select one of the sound resources and click the [Upload Audio] button. After uploading, you can listen to the sound or intercept a certain sound segment. After confirmation, click the [Upload Audio] button.
![Upload audio](images/image-clone-integration-02.png)

After uploading the audio, you will see in the list that the corresponding timbre will become "to be reproduced". Click the [Replicate Now] button. Wait 1~2 seconds for the result to be returned.

If the copy fails, please place the mouse on the "Error Message" icon and the reason for the failure will be displayed.

If the copy is successful, you will see that the corresponding tone in the list will change to "Training Successful" status. At this time, you can click the modify button in the [Sound Name] column to modify the name of the sound resource to facilitate later selection and use.

## The fourth stage: use stage

Click [Agent Management] at the top, select any agent, and click the [Configure Role] button.

For speech synthesis (TTS), select "Volcano dual-stream speech synthesis". In the list, find the sound resource with the name "Clone Sound" (as shown in the picture), select it, and click Save.
![Select tone](images/image-clone-integration-03.png)

Next, you can wake up Xiaozhi and talk to it.
