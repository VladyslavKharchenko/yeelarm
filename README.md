## Description
___
The main purpose of the script is to **simulate sunrise** using **Yeelight** bulb. 
It'll allow to wake up more naturally and gently.   
«Sunlight in the morning affects your circadian rhythm, setting your body clock for the day and 
signaling you that it's time to wake up... the retinas in our eyes have light-sensitive cells called photoreceptors that 
tell the brain whether it’s daytime or nighttime and thus affects our sleep cycle...». [[1]](#references)
## Usage
___
In order to use the script please perform the following steps
1. Update bulb firmware to the **latest** version
2. Install [yeelight](https://gitlab.com/stavros/python-yeelight.git)
3. Clone the repository
4. Execute `python3 main.py`
5. Follow the instructions
## Notes
___
The script have been tested using  
* Python 3.9.2
* yeelight v0.5.4 (2020-10-08)
* Xiaomi Yeelight Smart LED Bulb Color 1S (YLDP13YL)
* Firmware 2.0.6_0034  

Would like to recall that it's crucial to use the latest bulb firmware because some releases before `2.0.6_0034` 
might have various network issues.
## References
___
[1] - [What Happens In Your Brain When You Wake Up To Sunlight](https://www.bustle.com/p/waking-up-to-sunlight-does-this-to-your-brain-19448915)
