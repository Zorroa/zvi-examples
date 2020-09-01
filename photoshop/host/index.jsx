// https://www.adobe.com/content/dam/acom/en/devnet/photoshop/pdfs/photoshop-javascript-ref-2020.pdf
// https://github.com/ExtendScript/wiki/wiki/Executing-Shell-Commands
try {
    var xLib = new ExternalObject("lib:PlugPlugExternalObject");
} catch (e) {
    alert(e);
}

function openDocument(extRoot, id) {
    var fileRef = new File(
        extRoot + "/assets/" + id
    );
    app.open(fileRef);
}