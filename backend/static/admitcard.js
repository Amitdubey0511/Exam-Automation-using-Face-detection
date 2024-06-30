document.addEventListener("DOMContentLoaded", function() {
    // Sample data (replace with your actual data)
    const teacherDetails = {
      id: "T12345",
      examDate: "2024-03-01",
      day: "Monday",
      time: "09:00 AM",
      duration: "2 hours",
      venue: "Room 101"
    };
  
    const students = [
      { id: "S001", name: "John Doe", class: "10A" },
      { id: "S002", name: "Jane Smith", class: "10B" },
      { id: "S003", name: "Alice Johnson", class: "10C" }
      // Add more students as needed
    ];
  
    // Populate teacher details
    document.getElementById("teacher-id").textContent = teacherDetails.id;
    document.getElementById("exam-date").textContent = teacherDetails.examDate;
    document.getElementById("exam-day").textContent = teacherDetails.day;
    document.getElementById("exam-time").textContent = teacherDetails.time;
    document.getElementById("exam-duration").textContent = teacherDetails.duration;
    document.getElementById("exam-venue").textContent = teacherDetails.venue;
  
    // Populate students table
    const studentsTableBody = document.getElementById("students-body");
    students.forEach(student => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${student.id}</td>
        <td>${student.name}</td>
        <td>${student.class}</td>
      `;
      studentsTableBody.appendChild(row);
    });
  });
  