cd /workspaces/WAHID-Platform/backend
echo "python-3.12" > runtime.txt
git add runtime.txt
git commit -m "fix: spécifier Python 3.12 pour compatibilité wheels"
git push origin main