document.addEventListener('DOMContentLoaded', function() {
    const form1 = document.getElementById('dynamicForm');
    const form2 = document.getElementById('form')
    const fieldsContainer = document.getElementById('fieldsContainer');
    const addFieldButton = document.getElementById('addField');

    // Function to add new field
    function addField() {
      const newField = document.createElement('div');
      newField.classList.add('field-group');
      newField.innerHTML = `
        <select name="product[]" required>
            <option value=""selected disabled hidden>SELECT MEDICINE</option>
                {% block desg %}
                    {% for item in items %}
                        <option value="{{ item }}">{{ item[0] }}</option>
                    {% endfor %}
                {% endblock %}
        </select>
        <input type="text" name="rate[]" placeholder="Enter Rate*" required>
        <input type="number" name="quantity[]" placeholder="Enter Quantity*" required>
        <button class="remove-field" id="remove">Remove</button>
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
    form1.addEventListener('submit', async function(event) {
      event.preventDefault();
      const formData1 = new FormData(form1);
      const formData2 = new FormData(form2);
      const combinedFormData = new FormData();
      console.log(formData2)

      // Combine data from both forms
      for (const [key, value] of formData1) {
        combinedFormData.append(key, value);
      }
      for (const [key, value] of formData2) {
        combinedFormData.append(key, value);
      }

      try {
        const response = await fetch('/purchase_register', {
          method: 'POST',
          body: combinedFormData
        });
        const data = await response.json();
        console.log(data);
      } catch (error) {
        console.error('Error:', error);
      }
    });
  });