console.log('hello word video')
btn = document.getElementById('btn-demo')
btn.addEventListener('click', () => {
    html = `
            <video src="satatic/media/video_demo_sistema_recomendador.mp4" controls width="430" height="430"></video>
        `
    document.getElementById('target-demo').innerHTML = html
})