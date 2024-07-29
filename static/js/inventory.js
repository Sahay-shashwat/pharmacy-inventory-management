$(document).ready(function() {
    function createTableRow(item) {
        return `
            <tr>
                <td>${item.value[0]}</td>
                <td>${item.value[1]}</td>
                <td>${item.value[2]}</td>
                <td>${item.value[3]}</td>
                <td>${item.value[4]}</td>
            </tr>
        `;
    }
    
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
                        console.log(item.value[0])
                        $('#table-body').append(createTableRow(item));
                    });
                },
                error: function(xhr, status, error) {
                    console.error('Error occurred:', error);
                }
            });
        }
    });
});
