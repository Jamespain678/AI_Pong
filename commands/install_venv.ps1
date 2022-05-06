$this_folder = $MyInvocation.MyCommand.Path
$project_folder = "$this_folder - \..\..\"
cd $project_folder
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt