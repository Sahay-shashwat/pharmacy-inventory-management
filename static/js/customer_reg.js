document.addEventListener('DOMContentLoaded', function() {
    const form1 = document.getElementById('dynamicForm');
    const form2 = document.getElementById('form')
    const fieldsContainer = document.getElementById('fieldsContainer');
    const addFieldButton = document.getElementById('addField');


    function validateQuantity(quantity,medicine,MRP,Exp_date) {
      const enteredQuantity=quantity;
      $.ajax({
          type: 'GET',
          url: '/get_available_quantity',
          data: {
            medicine: medicine,
            MRP:MRP,
            Exp_date:Exp_date
          },
          success: function(response) {
              const availableQuantity = response.available_quantity;
              if (enteredQuantity > availableQuantity) {
                  alert('Quantity exceeds available stock!');
                  $('#Quantity').val('');
              }
          },
          error: function(xhr, status, error) {
            console.error('Error:', error);
          }
      });
    }


    fieldsContainer.addEventListener('input', function(event) {
      if (event.target.classList.contains('Quantity-select')) {
        const quantity = event.target.value;
        const fieldGroup = event.target.closest('.field-group');
        const medicine = fieldGroup.querySelector('.medicine-select').value;
        const MRP = fieldGroup.querySelector('.MRP-select').value;
        const Exp_date = fieldGroup.querySelector('.Exp_date-select').value;
        validateQuantity(quantity, medicine, MRP, Exp_date);
      }
    });
    
    function addField() {
      const newField = document.createElement('div');
      newField.classList.add('field-group');
          newField.innerHTML = `
            <div class="field">
                <label for="medicine">Medicine<span class="required">*</span></label><br>
                <select name="product[]" class="medicine-select" name="medicine"></select>
            </div>
            
            <div class="field">
                <label for="MRP">MRP<span class="required">*</span></label><br>
                <select name="MRP[]" class="MRP-select"></select>
            </div>

            <div class="field">
                <label for="Exp_date">Exp Date<span class="required">*</span></label><br>
                <select name="Exp_date[]" class="Exp_date-select"></select>
            </div>
            
            <div class="field">
                <label for="Quantity">Quantity<span class="required">*</span></label><br>
                <input type="number" name="quantity[]" class="Quantity-select" placeholder="Enter Quantity *" required min="1">
            </div>
            
            <div class="field">
                <label for="Discount">Discount %</label><br>
                <input type="number" name="Discount[]" id="Discount" placeholder="Enter Discount%" min="0">
            </div>
            
                <label for="remove"></label>
                <button class="remove-field" id="remove">Remove</button>
      `;
      fieldsContainer.appendChild(newField);

      $.ajax({
        type: 'GET',
        url: '/get_items_customer',
        dataType: 'json',
        timeout:5000,
      }).then(function(data) {
            var items=data;
            const selectElement = newField.querySelector('.medicine-select');
            $(selectElement).empty();
            $(selectElement).append(`<option value="" selected disabled hidden>SELECT MEDICINE</option>`);
            items.forEach(function(option) {
                $(selectElement).append(`<option value="${option.text}">${option.text}</option>`);
            });
            
            $(selectElement).on('change', function() {
                const Product_Name = $(this).val();
                    $.ajax({
                        type: 'GET',
                        url: `/getMRP?product=${Product_Name}`,
                        dataType: 'json',
                    }).then(function(data) {
                            var items=data;
                            $('.MRP-select').empty();
                            $('.MRP-select').append(`<option value="" selected disabled hidden>SELECT MRP</option>`);
                            items.forEach(function(option) {
                                $('.MRP-select').append(`<option value="${option.MRP}">${option.MRP}</option>`);
                            });
                        });
              $('.MRP-select').on('change',function(){
                const medicine = $('.medicine-select').val();
                const MRP = $('.MRP-select').val();
                    $.ajax({
                      type: 'GET',
                      url: `/getExpDate`,
                      data:{
                        medicine: medicine,
                        MRP: MRP
                      },
                      timeout:5000,
                      }).then(function(data) {
                          var items=data;
                          $('.Exp_date-select').empty();
                          $('.Exp_date-select').append(`<option value="" selected disabled hidden>SELECT EXPIRY DATE</option>`);
                          items.forEach(function(option) {
                              $('.Exp_date-select').append(`<option value="${option.ExpDate}">${option.ExpDate}</option>`);
                          });
                      });
                    });   
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

      // Combine data from both forms
      for (const [key, value] of formData1) {
        combinedFormData.append(key, value);
      }
      for (const [key, value] of formData2) {
        combinedFormData.append(key, value);
      }

      try {
        const response = await fetch('/customer_register', {
          method: 'POST',
          body: combinedFormData
        });
        if(!response.ok){
          throw new Error('HTTP error! status: ${response.status}')
        }
        const data = await response.json();
        window.location.href = '/dashboard';
      } catch (error) {
        console.error('Error:', error);
      }
    });
  });

  async function getMRP(Product_Name){
    $.ajax({
        type: 'GET',
        url: `/getMRP?product=${Product_Name}`,
        dataType: 'json',
        timeout:5000,
    }).then(function(data) {
            var items=data;
            $('#MRP').empty();
            $('#MRP').append(`<option value="" selected disabled hidden>SELECT MRP</option>`);
            items.forEach(function(option) {
                $('#MRP').append(`<option value="${option.MRP}">${option.MRP}</option>`);
            });
        });
  }

  async function getExpDate(MRP,medicine){
    $.ajax({
        type: 'GET',
        url: `/getExpDate`,
        data:{
          medicine: medicine,
          MRP: MRP
        },
        timeout:5000,
        }).then(function(data) {
            var items=data;
            $('#Exp_date').empty();
            $('#Exp_date').append(`<option value="" selected disabled hidden>SELECT EXPIRY DATE</option>`);
            items.forEach(function(option) {
                $('#Exp_date').append(`<option value="${option.ExpDate}">${option.ExpDate}</option>`);
            });
        });
  }

function validateQuantity(quantity,medicine,MRP,Exp_date) {
  const enteredQuantity=quantity;
  $.ajax({
      type: 'GET',
      url: '/get_available_quantity',
      data: {
        medicine: medicine,
        MRP:MRP,
        Exp_date:Exp_date
      },
      success: function(response) {
          const availableQuantity = response.available_quantity;
          if (enteredQuantity > availableQuantity) {
              alert('Quantity exceeds available stock!');
              $('#Quantity').val('');
          }
      }
  });
}
