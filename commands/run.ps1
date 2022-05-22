$this_folder = $MyInvocation.MyCommand.Path
$project_folder = "$this_folder - \..\..\"
cd $project_folder
.\venv\Scripts\Activate.ps1
python .\python\main.py $args[0] $args[1]