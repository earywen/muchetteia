import subprocess
import json
import os
import sys

# Chemins de base vers vos skills
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(PROJECT_ROOT, "skills")

def run_agent_script(skill_name, script_name, args=None):
    """
    Exécute un script Python situé dans le dossier d'un agent.
    """
    script_path = os.path.join(SKILLS_DIR, skill_name, "scripts", script_name)
    
    if not os.path.exists(script_path):
        return {"status": "error", "message": f"Script non trouvé : {script_path}"}
    
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}
    except json.JSONDecodeError:
        return {"status": "error", "message": "Erreur de décodage JSON du script"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
