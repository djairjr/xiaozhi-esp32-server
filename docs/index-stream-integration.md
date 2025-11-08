# IndexStreamTTS Usage Guide

## Environment preparation
### 1. Clone project
```bash 
git clone https://github.com/Ksuriuri/index-tts-vllm.git
```
Enter the unzipped directory
```bash
cd index-tts-vllm
```
Switch to the specified version (use the historical version of VLLM-0.10.2)
```bash
git checkout 224e8d5e5c8f66801845c66b30fa765328fd0be3
```

### 2. Create and activate conda environment
```bash 
conda create -n index-tts-vllm python=3.12
conda activate index-tts-vllm
```

### 3. Installing PyTorch requires version 2.8.0 (the latest version)
#### Check the highest supported version of the graphics card and the actual installed version
```bash
nvidia-smi
nvcc --version
``` 
#### The highest CUDA version supported by the driver
```bash
CUDA Version: 12.8
```
#### Actual installed CUDA compiler version
```bash
Cuda compilation tools, release 12.8, V12.8.89
```
#### Then the corresponding installation command (pytorch defaults to the 12.8 driver version)
```bash
pip install torch torchvision
```
Requires pytorch version 2.8.0 (corresponding to vllm 0.10.2). For specific installation instructions, please refer to: [pytorch official website](https://pytorch.org/get-started/locally/)

### 4. Install dependencies
```bash 
pip install -r requirements.txt
```

### 5. Download model weights
### Option 1: Download the official weight file and convert it
This is the official weight file. You can download it to any local path. It supports the weight of IndexTTS-1.5.
| HuggingFace                                                   | ModelScope                                                          |
|---------------------------------------------------------------|---------------------------------------------------------------------|
| [IndexTTS](https://huggingface.co/IndexTeam/Index-TTS)        | [IndexTTS](https://modelscope.cn/models/IndexTeam/Index-TTS)        |
| [IndexTTS-1.5](https://huggingface.co/IndexTeam/IndexTTS-1.5) | [IndexTTS-1.5](https://modelscope.cn/models/IndexTeam/IndexTTS-1.5) |

The following takes the installation method of ModelScope as an example.
#### Please note: git needs to be installed and initialized to enable lfs (you can skip it if it is already installed)
```bash
sudo apt-get install git-lfs
git lfs install
```
Create a model directory and pull the model
```bash 
mkdir model_dir
cd model_dir
git clone https://www.modelscope.cn/IndexTeam/IndexTTS-1.5.git
```

#### Model weight conversion
```bash 
bash convert_hf_format.sh /path/to/your/model_dir
```
For example: the IndexTTS-1.5 model you downloaded is stored in the model_dir directory, then execute the following command
```bash
bash convert_hf_format.sh model_dir/IndexTTS-1.5
```
This operation will convert the official model weights into a version compatible with the transformers library, and save them in the vllm folder under the model weight path to facilitate subsequent loading of model weights by the vllm library.

### 6. Change the interface to adapt to the project
The data returned by the interface is not suitable for the project and needs to be adjusted so that it can directly return audio data.
```bash
vi api_server.py
```
```bash 
@app.post("/tts", responses={
    200: {"content": {"application/octet-stream": {}}},
    500: {"content": {"application/json": {}}}
})
async def tts_api(request: Request):
    try:
        data = await request.json()
        text = data["text"]
        character = data["character"]

        global tts
        sr, wav = await tts.infer_with_ref_audio_embed(character, text)

        return Response(content=wav.tobytes(), media_type="application/octet-stream")
        
    except Exception as ex:
        tb_str = ''.join(traceback.format_exception(type(ex), ex, ex.__traceback__))
        print(tb_str)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(tb_str)
            }
        )
```

### 7. Write the sh startup script (please note that it must be run in the corresponding conda environment)
```bash 
vi start_api.sh
```
### Paste the following content and press: Enter wq to save
#### Please modify /home/system/index-tts-vllm/model_dir/IndexTTS-1.5 in the script to the actual path.
```bash
# Activate conda environment
conda activate index-tts-vllm 
echo "Activate project conda environment"
sleep 2
# Find the process ID occupying port 11996
PID_VLLM=$(sudo netstat -tulnp | grep 11996 | awk '{print $7}' | cut -d'/' -f1)

# Check if the process number is found
if [ -z "$PID_VLLM" ]; then
echo "The process occupying port 11996 was not found"
else
echo "Find the process occupying port 11996, the process number is: $PID_VLLM"
# Try normal kill first, wait 2 seconds
  kill $PID_VLLM
  sleep 2
# Check if the process is still there
  if ps -p $PID_VLLM > /dev/null; then
echo "The process is still running, force termination..."
    kill -9 $PID_VLLM
  fi
echo "Terminated process $PID_VLLM"
fi

# Find processes occupying VLLM::EngineCore
GPU_PIDS=$(ps aux | grep -E "VLLM|EngineCore" | grep -v grep | awk '{print $2}')

# Check if the process number is found
if [ -z "$GPU_PIDS" ]; then
echo "No VLLM related process found"
else
echo "Found the VLLM related process, the process number is: $GPU_PIDS"
# Try normal kill first, wait 2 seconds
  kill $GPU_PIDS
  sleep 2
# Check if the process is still there
  if ps -p $GPU_PIDS > /dev/null; then
echo "The process is still running, force termination..."
    kill -9 $GPU_PIDS
  fi
echo "Terminated process $GPU_PIDS"
fi

#Create tmp directory (if it does not exist)
mkdir -p tmp

# Run api_server.py in the background and redirect the log to tmp/server.log
nohup python api_server.py --model_dir /home/system/index-tts-vllm/model_dir/IndexTTS-1.5 --port 11996 > tmp/server.log 2>&1 &
echo "api_server.py is running in the background, please check tmp/server.log for the log"
```
Give the script execute permission and run the script
```bash 
chmod +x start_api.sh
./start_api.sh
```
The log will be output in tmp/server.log. You can check the log status through the following command
```bash
tail -f tmp/server.log
```
If the graphics card memory is sufficient, you can add the startup parameter ----gpu_memory_utilization in the script to adjust the graphics memory usage ratio. The default value is 0.25

## Tone configuration
index-tts-vllm supports registration of custom timbres through configuration files, and supports single timbre and mixed timbre configuration.
Configure custom sounds in the assets/speaker.json file in the project root directory
### Configuration format description
```bash
{
"Speaker Name 1": [
"Audio file path 1.wav",
"Audio file path 2.wav"
    ],
"Speaker Name 2": [
"Audio file path 3.wav"
    ]
}
```
### Note (after configuring the role, you need to restart the service to register the sound)
After adding, you need to add the corresponding speaker in the intelligent console (for a single module, replace the corresponding voice)