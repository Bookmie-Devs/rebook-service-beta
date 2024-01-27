const items = document.querySelectorAll('.item')

window.addEventListener('load', ()=>{
    document.querySelectorAll('.contain').forEach((contain) => {
      contain.style.display = 'none'
    })
    document.querySelector(`.container0`).style.display = 'flex';
})

function showContainer(containerNumber) {
    document.querySelectorAll('.contain').forEach((contain) => {
      contain.style.display = 'none'
    })

    document.querySelector(`.container${containerNumber}`).style.display = 'flex';
}

document.querySelectorAll('.bttn').forEach((item, index) => item.addEventListener('click', ()=>{
  document.querySelector(`#card${index+1}`).showModal()
}))

document.querySelectorAll('.submit').forEach((item, index) => item.addEventListener('click', (e)=>{
  e.preventDefault()
  document.querySelector(`#card${index+1}`).close()
}))

document.querySelectorAll('.exit').forEach((item, index) => item.addEventListener('click', (e)=>{
  e.preventDefault()
        document.querySelector(`#card${index+1}`).close()
      }))
      
 document.querySelector('.change-btn').addEventListener('click', (e)=>{
  e.preventDefault()
})
      
// function show(no){
//   document.querySelector(`#card${no}`).showModal()
// }

// function exit(no){
//   document.querySelector(`#card${no}`).close()
// }
