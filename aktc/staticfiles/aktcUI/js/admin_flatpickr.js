

console.log("Flatpickr JS loaded!");



// // static/events/js/admin_flatpickr.js
// document.addEventListener('DOMContentLoaded', function () {
//   const fields = document.querySelectorAll("input[data-flatpickr='true']");
//   if (fields.length > 0) {
//     fields.forEach(field => {
//       flatpickr(field, {
//         dateFormat: "Y-m-d",
//         minDate: "today",
//         disable: ["2025-07-10", "2025-07-15"]
//       });
//     });
//   } else {
//     console.warn("No flatpickr-enabled fields found");
//   }
// });



document.addEventListener("DOMContentLoaded", function (e) {
  
  flatpickr("input[type='text'][data-flatpickr='true']", {
        dateFormat: "Y-m-d",
        onChange: function(selectedDates, dateStr, instance){
          
          fetch('/select-depature/', {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
              "X-CSRFToken": getCookie('csrftoken')
            },
            body: new URLSearchParams({date: dateStr})
          })
          .then(response => response.json())
          .then(data => {

            console.log(`onChange: date worked`)
            console.log(data)
            console.log(data.daily_schedule)
            const bookingDepartureTime = document.querySelector('#booking-departure-time');
            // console.log(bookingDepartureTime.)
            bookingDepartureTime.innerHTML = ''
            if (!data.daily_schedule) {
              bookingDepartureTime.innerHTML += '<option value="---------------">---------------</option>' 
              // bookingDepartureTime.disable
              `send a response back that they is no schedule for that day, 
              
              although we will still use calendar to prevent some ishes`
            } else {
              data.daily_schedule.forEach(element => {
                const departureTime = `${element.hour}:${element.minute}${element.meridian}`
                bookingDepartureTime.innerHTML += `<option value="${departureTime}">${departureTime}</option>` 
                
              });
              //   `
              // console.log(bookingDepartureTime)
              // <option value=${dateStr}>${dateStr}<option/>
              // `
              

            }
            
          })
          
        },
        minDate: "today", // optional
        disable: ["2025-07-10", "2025-07-15"] // example disabled dates

      });

      function getCookie(){

      }

  




  

});

