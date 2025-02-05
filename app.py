from scripts.modeldownloader import install_deepspeed_based_on_python_version
from argparse import ArgumentParser
from loguru import logger
import os
import subprocess

parser = ArgumentParser(description="Run the Uvicorn server.")
parser.add_argument("-hs", "--host", default="127.0.0.1", help="Host to bind")
parser.add_argument("-p", "--port", default=8010,
                    type=int, help="Port to bind")
parser.add_argument("-sf", "--speaker_folder", default="speakers/",
                    type=str, help="The folder where you get the samples for tts")
parser.add_argument("-o", "--output", default="output/",
                    type=str, help="Output folder")
parser.add_argument("-l", "--language", default="Auto",
                    type=str, help="WebUI language")
parser.add_argument("-ms", "--model-source", default="local", choices=["api", "local"],
                    help="Define the model source: 'api' for latest version from repository, api inference or 'local' for using local inference and model v2.0.2.")
parser.add_argument("-v", "--version", default="v2.0.2", type=str,
                    help="You can specify which version of xtts to use,This version will be used everywhere in local, api and apiManual.")
parser.add_argument("--share", action='store_true',
                    help="Allows the interface to be used outside the local computer.")
parser.add_argument("--rvc", action='store_true',
                    help="Choose extensions what you add to main webui [-e rvc]")

args = parser.parse_args()

# Set environment variable for output folder.
os.environ['OUTPUT'] = args.output
# Set environment variable for speaker folder.
os.environ['SPEAKER'] = args.speaker_folder
os.environ['BASE_URL'] = "http://" + args.host + ":" + \
    str(args.port)  # Set environment variable for base url."
# Set environment variable for the model source
os.environ['MODEL_SOURCE'] = args.model_source
os.environ["MODEL_VERSION"] = args.version  # Specify version of XTTS model

os.environ["LANGUAGE"] = args.language 

os.environ["RVC_ENABLED"] = str(args.rvc).lower()

# Install RVC
if args.rvc:
    # Create rvc folder
    os.makedirs("rvc", exist_ok=True)
    if (not os.path.exists("venv/rvc_venv")):
        logger.info("Installing RVC and OpenVoice libraries...")
        subprocess.run(["python", "scripts/install_rvc_venv.py"])
        logger.info("RVC and OpenVoice installation is complete")
    # else:
        # logger.info("RVC libraries are already installed")

# Check deepspeed
install_deepspeed_based_on_python_version()

if __name__ == "__main__":
    from xtts_webui import demo
    demo.launch(share=args.share, inbrowser=True,
                server_name=args.host, server_port=args.port)
