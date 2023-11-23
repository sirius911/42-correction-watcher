# 42 correction watcher

A Python script that will send you a desktop notification when a correction slot is found.

From [t0mm4rx](https://github.com/t0mm4rx/42-correction-watcher)

## Usage

Only tested on macOS.
```sh
# Use python 3
pip3 install -r requirements.txt
python3 watcher.py
```

## Where to find the needed data?
- project URL: in the URL of the correction board (projects.intra.42.fr/projects/**42cursus-ft_linear_regression**/slots?team_id=3547579 => 42cursus-ft_linear_regression).
- team ID: in the URL of the correction board (projects.intra.42.fr/projects/42cursus-ft_linear_regression/slots?team_id=**3547579** => 3547579).
- session token: in your cookies on the intra, under the name **_intra_42_session_production**.
- api callback (optional): specify an url to call if a correction is found, use `{}` as a placeholder for the message. Example => "https://smsapi.free-mobile.fr/sendmsg?user=[censored]&pass=[censored]&msg={}"
