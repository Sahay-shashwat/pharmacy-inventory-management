$(document).ready(function() {
    $('#inventory').on('keyup', function() {
        var searchQuery = $(this).val();
        if (searchQuery.length > 0) {
            $.ajax({
                type: 'GET',
                url: '/inventory',
                data: { inventory: searchQuery },
                success: function(data) {
                    $('#table-body').empty();
                    $.each(data, function(index, item) {
                        $('#table-body').append(`
                            <tr>
                                <td>${item.medicine_name}</td>
                                <td>${item.manf_date}</td>
                                <td>${item.expiry_date}</td>
                                <td>${item.mrp}</td>
                                <td>${item.quantity}</td>
                            </tr>
                        `);
                    });
                }
            });
        }
    });
});