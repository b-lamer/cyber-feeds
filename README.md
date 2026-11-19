## Overview
This program will scrape cybersecurity news and KEV vulnerability releases and print the latest updates on a streamlit display.<br>

To utilize the full program, you will need to do the following based on the version you want:<br>


### Docker (Recommended):
- Build image: `docker build -t cyberfeed .`
- Run container: `docker run -d -p 8501:8501 cyberfeed`

**OR** Download the public image here: https://hub.docker.com/r/sblam/cyberfeed

### Windows/Linux:
- Install Dependencies: `pip install -r requirements.txt`
- Run program: `streamlit run dashboard.py` (in program directory)


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Example
Below is my use case of this program. It is run on a Raspberry Pi 3 connected to a 7-inch display which is held up by two 3D printed stands. 
<br>
<br>
![7 Inch News Feed](https://github.com/user-attachments/assets/2dce950e-4441-4ad2-8b3c-6d20da8829ad)