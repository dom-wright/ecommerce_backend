const container = document.getElementById("video-container")
const buttonElem = document.getElementById("button-elem")
const videoElem = document.getElementById("video-elem")

buttonElem.addEventListener('click', makeRequest)
console.log('script ran')

function makeRequest(event) {
    console.log('this is working')
    const url = '/video'
    console.log(url)
    const response = fetch(url)
        .then((response) => response.blob())
        .then((myBlob) => {
            videoElem.src = URL.createObjectURL(myBlob);
        });
}