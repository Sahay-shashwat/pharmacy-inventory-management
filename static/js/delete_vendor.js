function getGST(Vendor_Name){
    var vendorName = Vendor_Name
    $.ajax({
        type: 'GET',
        url: `/getGST?vendor=${vendorName}`,
        dataType: 'json',
        timeout:5000,
    }).then(function(data) {
            var items=data;
            $('#GST').empty();
            $('#GST').append(`<option value="" selected disabled hidden>SELECT GST</option>`);
            items.forEach(function(option) {
                $('#GST').append(`<option value="${option.GST}">${option.GST}</option>`);
            });
        });
  }