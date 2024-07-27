document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('dynamicForm');
    const fieldsContainer = document.getElementById('fieldsContainer');
    const addFieldButton = document.getElementById('addField');
  
    // Function to add new field
    function addField() {
      const newField = document.createElement('div');
      newField.classList.add('field-group');
      newField.innerHTML = `
        <input type="text" name="field[]" placeholder="Enter something">
        <button class="remove-field">Remove</button>
      `;
      fieldsContainer.appendChild(newField);
    }
  
    // Function to remove field
    function removeField(event) {
      if (event.target.classList.contains('remove-field')) {
        const fieldGroup = event.target.parentNode;
        fieldsContainer.removeChild(fieldGroup);
      }
    }
  
    // Add event listener to the add field button
    addFieldButton.addEventListener('click', addField);
  
    // Add event listener for removing fields
    fieldsContainer.addEventListener('click', removeField);
  
    // Handle form submission
    form.addEventListener('submit', function(event) {
      event.preventDefault();
      const formData = new FormData(form);
      fetch('/submit', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
    });
  });