
const imgBox = document.getElementById('image')
const image = document.getElementById('id_profile_pic')

image.addEventListener('change', ()=>{
    const img_data = image.files[0]
    const url = URL.createObjectURL(img_data)
    console.log(url)
    imgBox.innerHTML = `<img class="image" src="${url}" width="100%">`
})