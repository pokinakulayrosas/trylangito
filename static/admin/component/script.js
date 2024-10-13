const calendar = document.querySelector(".calendar"),
    date = document.querySelector(".date"),
    daysContainer = document.querySelector(".days"),
    prev = document.querySelector(".prev");
    next = document.querySelector(".next"),
    todayBtn = document.querySelector(".today-btn"),
    gotoBtn = document.querySelector(".goto-btn"),
    dateInput = document.querySelector(".date-input"),
    eventDay = document.querySelector(".event-day"),
    eventDate = document.querySelector(".event-date"),
    eventsCont = document.querySelector(".events"),
    addSubmit = document.querySelector(".add-event-btn");

let today = new Date();
let activeDay;
let month = today.getMonth();
let year = today.getFullYear();

const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
];

let eventsArr = [];

getEvents();

//function to add days
function initCalendar(){
    //to get prev month days and current month all days and rem next month days
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const prevLastDay = new Date (year, month, 0);
        const prevDays = prevLastDay.getDate();
        const lastDate = lastDay.getDate();
        const day = firstDay.getDay();
        const nextDays = 7 - lastDay.getDay() - 1;

        //update date top of calendar
        date.innerHTML = months[month] + " " + year;

        //adding days on dom
        let days = "";

        for(let x = day; x > 0; x--){
            days += `<div class="day prev-date">${prevDays - x + 1}</div>`;
        }

        //current month days


        for(let i = 1; i<=lastDate; i++){

            let event = false;
            eventsArr.forEach((eventObj)=>{
                if(eventObj.day == i &&
                eventObj.month == month + 1 &&
            eventObj.year == year){
                event = true;
            }
            })

            //if day is today add class today
            if(i == new Date().getDate() && 
            year == new Date().getFullYear() && 
            month == new Date().getMonth()){

                activeDay = i;
                getActiveDay(i);
                updateEvents(i);
                if(event){
                    days += `<div class="day today active event">${i}</div>`;
                }else{
                    days += `<div class="day today active">${i}</div>`;
                }
            }
            else{
                if(event){
                    days += `<div class="day event">${i}</div>`;
                }else{
                    days += `<div class="day">${i}</div>`;
                }
            }
        }

        for (let j = 1; j <= nextDays; j++){
            days += `<div class="day next-date" >${j}</div>`;
        }

            daysContainer.innerHTML = days;
            addListener();
}

initCalendar();

//prev month

function prevMonth(){
    month--;
    if(month < 0){
        month = 11;
        year--;
    }
    initCalendar();
}

//next month

function nextMonth(){
    month++;
    if(month > 11){
        month = 0;
        year++;
    }
    initCalendar();
}


//add eventlistener on prev and next

prev.addEventListener("click", prevMonth);
next.addEventListener("click", nextMonth);


todayBtn.addEventListener("click", () =>{
    today = new Date();
    month = today.getMonth();
    year = today.getFullYear();
    initCalendar();
});

dateInput.addEventListener("input", (e) =>{
    //allow only numbers
    dateInput.value = dateInput.value.replace(/[^0-9/]/g, "");
    if(dateInput.value.length == 2){
        //add a slash if two numbers entered
        dateInput.value += "/";
    }
    if(dateInput.value.length > 7){
        //don't allow more than 7 chars
        dateInput.value = dateInput.value.slice(0,7);
    }

    //if backspace is pressed
    if(e.inputType == " deleteContentBackward "){
        if(dateInput.value.length == 3) {
            dateInput.value = dateInput.value.slice(0,2);
        }
    }
});

gotoBtn.addEventListener("click", gotoDate);


function gotoDate(){
    const dateArr = dateInput.value.split("/");
    if(dateArr.length == 2){
        if(dateArr[0] > 0 && dateArr[0] < 13 && dateArr[1].length == 4){
            month = dateArr[0] - 1;
            year = dateArr[1];
            initCalendar();
            return;
        }
    }
    alert("invalid date");
}

const addEventBtn = document.querySelector(".add-event"),
    addEventContainer = document.querySelector(".add-event-wrapper"),
    addEventCloseBtn = document.querySelector(".close"),
    addEventTitle = document.querySelector(".event-name"),
    addEventFrom = document.querySelector(".event-time-from");
    addEventTo = document.querySelector(".event-time-to");

addEventBtn.addEventListener("click", () => {
    addEventContainer.classList.toggle("active");
});
addEventCloseBtn.addEventListener("click", () => {
    addEventContainer.classList.remove("active");
});

document.addEventListener("click", (e) => {
    if(e.target !== addEventBtn && !addEventContainer.contains(e.target)){
        addEventContainer.classList.remove("active");
    }
});

addEventTitle.addEventListener("input", (e) => {
    addEventTitle.value = addEventTitle.value.slice(0, 50);
});

addEventFrom.addEventListener("input", (e) =>{
    addEventFrom.value = addEventFrom.value.replace(/[^0-9:]/g, "");
    if(addEventFrom.value.length == 2){
        addEventFrom.value += ":";
    }
    if(addEventFrom.value.length > 5){
        addEventFrom.value = addEventFrom.value.slice(0.5);
    }
});

addEventTo.addEventListener("input", (e) =>{
    addEventTo.value = addEventTo.value.replace(/[^0-9:]/g, "");
    if(addEventTo.value.length == 2){
        addEventTo.value += ":";
    }
    if(addEventTo.value.length > 5){
        addEventTo.value = addEventTo.value.slice(0.5);
    }
});

function addListener() {
    const days = document.querySelectorAll(`.day`);
    days.forEach((day) => {
        day.addEventListener(`click`, (e) =>{
            activeDay = Number(e.target.innerHTML);

            getActiveDay(e.target.innerHTML);
            updateEvents(Number(e.target.innerHTML));

            days.forEach((day)=>{
                day.classList.remove(`active`);
            });

            if(e.target.classList.contains(`prev-date`)){
                prevMonth();

                setTimeout(()=>{
                    const days = document.querySelectorAll(`.day`);

                    days.forEach((day)=>{
                        if(!day.classList.contains(`prev-date`) && day.innerHTML == e.target.innerHTML){
                            day.classList.add(`active`);
                        }
                    });
                }, 100);
            } else if (e.target.classList.contains(`next-date`)){
                nextMonth();

                setTimeout(()=>{
                    const days = document.querySelectorAll(`.day`);

                    days.forEach((day)=>{
                        if(!day.classList.contains(`next-date`) && day.innerHTML == e.target.innerHTML){
                            day.classList.add(`active`);
                        }
                    });
                }, 100);
            } else {
                e.target.classList.add(`active`);
            }

        });
    });
}


function getActiveDay(date){
    const day = new Date(year, month, date);
    const dayName = day.toString().split(" ")[0];
    eventDay.innerHTML = dayName;
    eventDate.innerHTML = date + " " + months[month] + " " + year;
}

function updateEvents(date) {
    let events = "";
    eventsArr.forEach((event) => {
        if (date == event.day && month + 1 == event.month && year == event.year) {
            event.events.forEach((eventData) => {
                events += `
                <div class="event" data-new_id="${eventData.new_id}">
                    <div class="title">
                        <i class="fas fa-circle"></i>
                        <h3 class="event-title">${eventData.title} </h3>
                    </div>
                    <div class="event-time">
                        <span class="event-time">${eventData.time}</span>
                    </div>
                </div>
                `;
                console.log(`${eventData.new_id}`)
            });
        }
        console.log(event)
    });

    
    if (events === ""){
        events = `<div class="no-event">
            <h3>No Events</h3>
                </div>`;
    }
    eventsCont.innerHTML = events;

    saveEvents();
}

const generateID = () => {
    let numbers = '';
    for(let i = 0; i<10; i++){
        const randomNum = Math.floor(Math.random() * 10);
        numbers += randomNum;
    }
    return numbers;
}

addSubmit.addEventListener("click", async ()=>{
    const EventID = generateID();
    const eventTitle = addEventTitle.value;
    const eventTimeFrom = addEventFrom.value;
    const eventTimeTo = addEventTo.value;

    if(eventTitle == "" || eventTimeFrom == "" || eventTimeTo == ""){
        alert("Please Fill up the blank");
        return;
    }

    const timeFromArr = eventTimeFrom.split(":");
    const timeToArr = eventTimeTo.split(":");
    
    if(timeFromArr.length != 2 || 
        timeToArr.length != 2 || 
        timeFromArr[0] > 23 || 
        timeFromArr[1] > 59 || 
        timeToArr[0] > 23 || 
        timeToArr[1] > 59
    ){
        alert("Invalid Time Format");
    }

    const timeFrom = convertTime(eventTimeFrom);
    const timeTo = convertTime(eventTimeTo); 

    try {
        const response = await fetch('/api/events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                new_id: EventID,
                title: eventTitle,
                time: timeFrom + ' - ' + timeTo,
                date: eventDate.innerHTML 
            })
        });

        if (response.ok) {
            const eventData = await response.json();
            // newEvent._id = eventData._id;

            const newEvent = {
                new_id: EventID,
                _id: eventData._id,
                title: eventTitle,
                time: timeFrom + " - " + timeTo,
            };

            let eventAdded = false;

            if (eventsArr.length > 0) {
                eventsArr.forEach((item) => {
                    if (item.day == activeDay &&
                        item.month == month + 1 &&
                        item.year == year) {
                        item.events.push(newEvent);
                        eventAdded = true;
                    }
                });
            }
            if (!eventAdded) {
                eventsArr.push({
                    day: activeDay,
                    month: month + 1,
                    year: year,
                    events: [newEvent],
                });
            }

            // Clear input fields and update UI
            addEventContainer.classList.remove("active");
            addEventTitle.value = "";
            addEventFrom.value = "";
            addEventTo.value = "";
            updateEvents(activeDay);

            const activeDayElem = document.querySelector(".day.active");
            if (!activeDayElem.classList.contains("event")) {
                activeDayElem.classList.add("event");
            }
        } else {
            alert('Failed to add event');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while adding the event');
    }
});


function convertTime(time){
    let timeArr = time.split(":");
    let timeHour = timeArr[0];
    let timeMin = timeArr[1];
    let timeFormat = timeHour >= 12 ? "PM" : "AM";
    timeHour = timeHour % 12 || 12;
    time = timeHour + ":" + timeMin + " " + timeFormat;
    return time;
}

eventsCont.addEventListener("click", async (e) => {
    if(e.target.classList.contains("event")){
        console.log("Clicked Element:", e.target);
        console.log("Dataset:", e.target.dataset);
        const eventElement = e.target;
        const event_id = eventElement.dataset.new_id;
        console.log("Event ID:", event_id);

        const eventTitle = e.target.querySelector(".event-title").textContent;

        const confirmed = confirm(`Are you sure you want to remove the event "${eventTitle}"?`)
        if(!confirmed){
            return;
        }

        const response = await fetch(`/api/events?title=${eventTitle}`,{
            method: 'DELETE'
        });

        if(response.ok){
            alert("Event deleted successfully");
            eventsArr.forEach((event) => {
                if(event.day == activeDay &&
                event.month == month + 1 &&
                event.year == year){
                    event.events.forEach((item, index) => {
                        if(item.title == eventTitle) {
                            event.events.splice(index, 1);
                        }
                    });
                    if(event.events.length == 0){
                        eventsArr.splice(eventsArr.indexOf(event), 1);
                        
                        const activeDayElem = document.querySelector(".day.active")
                        if(activeDayElem.classList.contains("event")){
                            activeDayElem.classList.remove("event");
                        }
                    }
                }
                
            });
            updateEvents(activeDay);
        } else {
            alert("failed to delete event");
        }
    }
});

function saveEvents(){
    console.log("yes");
    localStorage.setItem("events", JSON.stringify(eventsArr));
}

function getEvents(){
    if(localStorage.getItem("events" == null)){
        return;
    }
    eventsArr.push( ... JSON.parse(localStorage.getItem("events")));
}
