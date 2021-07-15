const fs = require('fs');
const path = require('path');

function copy(from, to) {
	if (!fs.existsSync(to)) {
		fs.mkdirSync(to);
	}
	const files = fs.readdirSync(from);
	for (let file of files) {
		if (path.extname(file) === '.js') {
			const fromPath = path.join(from, file);
			const toPath = path.join(to, file);
			console.log(`copy ${fromPath} to ${toPath}`);
			fs.copyFileSync(fromPath, toPath);
		}
	}
}

let srcLocation = path.join(__dirname, '..', 'src');

const umdDir = path.join(__dirname, '..', 'lib', 'umd', 'beautify');
if (fs.existsSync(umdDir)) {
	copy(path.join(__dirname, '..', 'src', 'beautify'), umdDir);
}
const esmDir = path.join(__dirname, '..', 'lib', 'esm', 'beautify');
if (fs.existsSync(esmDir)) {
	copy(path.join(__dirname, '..', 'src', 'beautify', 'esm'), esmDir);
}
