
window.addEventListener('load', ()=>{
    document.querySelectorAll('.contan').forEach((contain) => {
      contain.style.display = 'none'
    })
    let current = sessionStorage.getItem('currentPage') || "0"
    document.querySelector(`.contaner${current}`).style.display = 'flex';
})

function showContainer(containerNumber) {
    document.querySelectorAll('.contan').forEach((contain) => {
      contain.style.display = 'none'
    })

    sessionStorage.setItem('currentPage', containerNumber)

    document.querySelector(`.contaner${containerNumber}`).style.display = 'flex';
}

document.querySelectorAll('.bttn').forEach((item) => item.addEventListener('click', ()=>{
  // console.log(item.dataset.id)
  document.querySelector(`#card${item.dataset.id}`).showModal()
}))

document.querySelectorAll('.submit').forEach((item) => item.addEventListener('click', (e)=>{
  e.preventDefault()
  document.querySelector(`#card${item.dataset.id}`).close()
}))

// document.querySelectorAll('.exit').forEach((item, index) => item.addEventListener('click', (e)=>{
//   e.preventDefault()
//         document.querySelector(`#card${index+1}`).close()
//       }))
      
//  document.querySelector('.change-btn').addEventListener('click', (e)=>{
//   e.preventDefault()
// })
      
// function show(no){
//   document.querySelector(`#card${no}`).showModal()
// }

// function exit(no){
//   document.querySelector(`#card${no}`).close()
// }
