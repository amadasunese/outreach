// Example for student enrollment
const enrollForm = document.getElementById('enrollForm'); // Get your form element

enrollForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(enrollForm);
    const data = {};
    formData.forEach((value, key) => data[key] = value); // Convert form data to JSON

    fetch('/enroll', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        alert(result.message); // Display success message
        enrollForm.reset(); // Clear the form
    })
    .catch(error => {
        console.error('Error enrolling student:', error);
        alert('An error occurred during enrollment.'); // Display error message to the user
    });
});

// Example for checking graduation
const checkGraduationButton = document.getElementById('checkGraduation');

checkGraduationButton.addEventListener('click', () => {
    const studentId = document.getElementById('studentId').value;

    fetch(`/check_graduation/${studentId}`)
        .then(response => response.json())
        .then(result => {
            // Display graduation results (e.g., in a div)
            const resultsDiv = document.getElementById('graduationResults');
            resultsDiv.innerHTML = `
                <p>Student ID: ${result.student_id}</p>
                <p>Attendance Percentage: ${result.attendance_percentage.toFixed(2)}%</p>
                <p>Average Score: ${result.average_score.toFixed(2)}%</p>
                <p>Qualified: ${result.qualified ? 'Yes' : 'No'}</p>
            `;
        })
        .catch(error => {
            console.error('Error checking graduation:', error);
            alert('An error occurred.');
        });
});

// ... (Similar JavaScript for mark_attendance and record_assessment)