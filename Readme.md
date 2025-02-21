1. Установка pyenv: Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
2. ([Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12)
3. pyenv install 3.13
4. pyenv global 3.13
5. Open bot directory
6. python -m venv .venv
7. .\.env\Scripts\activate
8. pip install aiogram 