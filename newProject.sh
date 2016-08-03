mkdir $1
cd $1
echo "# $1" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/ArizonaCyberWarfareRange/$1.git
git push -u origin master

