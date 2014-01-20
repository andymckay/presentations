# This checks out reveal.js and runs it. Each time you alter the files,
# re-run build.js. This requires node.
git clone https://github.com/hakimel/reveal.js.git
cd reveal.js
npm install
cp ../slides.md .
cp ../index.html .
rm -rf img
cp -r ../img .
grunt serve
