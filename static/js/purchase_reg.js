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
            <div class="field">
                <label for="medicine">Medicine<span class="required">*</span></label><br>
                <select name="product[]" class="medicine-select"></select>
            </div>

            <div class="field">
                <label for="Rate">Rate<span class="required">*</span></label><br>
                <input type="text" name="rate[]" id="Rate" placeholder="Enter Rate *" required>
            </div>

            <div class="field">
                <label for="Quantity">Quantity<span class="required">*</span></label><br>
                <input type="number" name="quantity[]" id="Quantity" placeholder="Enter Quantity *" required>
            </div>

            <div class="field">
                <label for="Manf_Date">Manf Date<span class="required">*</span></label><br>
                <input type="date" name="Manf_Date[]" id="Manf_Date" required>
            </div>

            <div class="field">
                <label for="Exp_date">Expiry Date<span class="required">*</span></label><br>
                <input type="date" id="Exp_date" name="Exp_date[]" required><br>
            </div>

            <div class="field">
                <label for="MRP">MRP<span class="required">*</span></label><br>
                <input type="text" name="MRP[]" id="MRP" placeholder="Enter MRP *" required>
            </div>
            
                <label for="remove"></label>
                <button class="remove-field" id="remove">Remove</button>
      `;
      fieldsContainer.appendChild(newField);

      $.ajax({
        type: 'GET',
        url: '/get_items',
        dataType: 'json',
        timeout:5000
      }).then(function(data) {
            var items=data;
            const selectElement = newField.querySelector('.medicine-select');
            $(selectElement).empty();
            $(selectElement).append(`<option value="" selected disabled hidden>SELECT MEDICINE</option>`);
            items.forEach(function(option) {
                $(selectElement).append(`<option value="${option.text}">${option.text}</option>`);
            });
        });
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
        if(!response.ok){
          throw new Error('HTTP error! status: ${response.status}')
        }
        const data = await response.json();
        console.log(data);
        window.location.href = '/dashboard';
      } catch (error) {
        console.error('Error:', error);
      }
    });
  });