document.addEventListener('DOMContentLoaded', function() {
    fetch('/referral_table')
        .then(response => response.json())
        .then(referrals => {
            const tbody = document.getElementById('referral-body');
            tbody.innerHTML = '';

            referrals.forEach(referral => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="clickable">${referral._id}</td>
                    <td>${referral.form1.fname} ${referral.form1.lname}</td>
                    <td>${referral.form2.date}</td>
                    <td>${referral.form2.college}</td>
                    <td class="primary" style="cursor: pointer;">Details</td>`;
                tbody.appendChild(tr);

                tr.querySelector('.clickable').addEventListener('click', function() {
                    window.location.href = `/referral_response/${referral._id}`;
                });
                tr.querySelector('.primary').addEventListener('click', function() {
                    window.location.href = `/referral_response/${referral._id}`;
                });
            });
        })
        .catch(error => console.error('Error fetching referrals:', error));
});

document.addEventListener("DOMContentLoaded", function() {

    // const tableBody = document.querySelector('.recent-orders table tbody');
    // const Students = [
    //     {
    //         fullName: "Elijah Cobarrubias",
    //         idNumber: "2023-154912",
    //         course: "BSIT",
    //         status: "Pending",
    //     },
    //     {
    //         fullName: "Alexandra Mae Manuzon",
    //         idNumber: "2023-154913",
    //         course: "BSIT",
    //         status: "Approved",
    //     },
    //     {
    //         fullName: 'Cha Gamboa',
    //         idNumber: '2023-154915',
    //         course: 'BSArchi',
    //         status: 'Cancelled'
    //     },
    // ];


    // fetch('/api/get/students')
    //     .then(response => response.json())
    //     .then(students => {
    //         students.forEach(student => {
    //             const tr = document.createElement('tr');
    //             tr.innerHTML = `
    //                 <td>${student.name}</td>
    //                 <td>${student.studentID}</td>
    //                 <td>${student.department}</td>
    //                 <td class="${student.status === 'Cancelled' ? 'danger' : student.status === 'Pending' ? 'warning' : 'primary'}">${student.status}</td>
    //                 <td>${student.date}</td>
    //                 <td class="primary" style="cursor: pointer;">Details</td>
    //             `;
    //             tableBody.appendChild(tr);
    //         });
    //     })
    //     .catch(error => console.error('Error fetching data:', error));

    const darkMode = document.querySelector('.dark-mode');


    darkMode.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode-variable');
        darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
        darkMode.querySelector('span:nth-child(2)').classList.toggle('active');

        drawChart();
    })

    function drawChart() {
        var chartContainer = document.getElementById("piechart");

        var data = google.visualization.arrayToDataTable([
          ["Task", "Hours per Day"],
          ["Sad", 11],
          ["Angry", 2],
          ["Happy", 2],
          ["Disgust", 2],
          ["Fear", 7],
        ]);

        var computedStyle = getComputedStyle(document.body);
        var backgroundColor = computedStyle.getPropertyValue("--color-white");
        var textColor = document.body.classList.contains('dark-mode-variable') ? '#fff' : '#000'
        var borderColor = document.body.classList.contains('dark-mode-variable') ? '#fff' : '#a3bdcc';
        
        var options = {
          backgroundColor: backgroundColor,
          legendTextStyle: {color: textColor},
          titleTextStyle: {color: textColor},
          pieSliceTextStyle: backgroundColor,
          pieSliceBorderColor: borderColor,
        };

        var chart = new google.visualization.PieChart(chartContainer);

        chart.draw(data, options);
      }

      drawChart();


    //   This if for example output of the status design
    
    // Students.forEach(student => {
    //     const tr = document.createElement('tr');
    //     const trContent = `
    //         <td>${student.fullName}</td>
    //         <td>${student.idNumber}</td>
    //         <td>${student.course}</td>
    //         <td class="${student.status === 'Cancelled' ? 'danger' : student.status === 'Pending' ? 'warning' : 'primary'}">${student.status}</td>
    //         <td class="primary">Details</td>
    //     `;
    //     tr.innerHTML = trContent;
    //     document.querySelector('table tbody').appendChild(tr);
    // });
});