echo "[ `date +%H:%M ` ]": "START"
echo "[ `date +%H:%M ` ]": "CREATING VIRTUAL ENV"
python3 -m venv env
echo "[ `date +%H:%M ` ]": "ACTIVATING VIRTUAL ENV"
source env/bin/activate
echo "[ `date +%H:%M ` ]": "INSTALLING REQUIREMENTS"
pip install -r requirements.txt
echo "[ `date +%H:%M ` ]": "INSTALLING PLAYWRIGHT"
playwright install
echo "[ `date +%H:%M ` ]": "END"
