import subprocess
import os
import sys
import venv

def run_command(command, description, env=None):
    print(f"\n--- {description} ---")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
        print(result.stdout)
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to run: {e}")
        return False

def setup_venv(target_dir):
    venv_dir = os.path.join(target_dir, ".audit_venv")
    if not os.path.exists(venv_dir):
        print(f"Criando ambiente virtual de auditoria em {venv_dir}...")
        venv.create(venv_dir, with_pip=True)
    
    # Determina o caminho do binário do python/pip no venv
    if os.name == 'nt': # Windows
        python_bin = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_bin = os.path.join(venv_dir, "Scripts", "pip.exe")
    else: # POSIX (Mac/Linux)
        python_bin = os.path.join(venv_dir, "bin", "python")
        pip_bin = os.path.join(venv_dir, "bin", "pip")
    
    # Instala ferramentas básicas de auditoria se necessário
    print("Garantindo ferramentas de auditoria (bandit, ruff, pip-audit)...")
    subprocess.run([pip_bin, "install", "bandit", "ruff", "pip-audit"], capture_output=True)
    
    # Tenta instalar requisitos do projeto se existirem
    req_file = os.path.join(target_dir, "requirements.txt")
    if os.path.exists(req_file):
        print(f"Instalando dependências do projeto de {req_file}...")
        subprocess.run([pip_bin, "install", "-r", req_file], capture_output=True)
    
    return python_bin

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    target_dir = os.path.abspath(target_dir)
    
    print(f"Iniciando auditoria técnica isolada em: {target_dir}")
    
    # Setup venv
    python_bin = setup_venv(target_dir)
    
    # 1. Django check --deploy (precisa do django instalado no venv)
    run_command(f"{python_bin} manage.py check --deploy", "Django Deployment Check")
    
    # 2. Safety/Bandit
    run_command(f"{python_bin} -m bandit -r {target_dir}", "Security Check (Bandit)")
    
    # 3. Ruff
    run_command(f"{python_bin} -m ruff check {target_dir}", "Lint Check (Ruff)")
    
    # 4. Pip audit
    run_command(f"{python_bin} -m pip_audit", "Package Vulnerability Check (pip-audit)")

if __name__ == "__main__":
    main()
