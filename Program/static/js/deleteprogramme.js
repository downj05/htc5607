function updateFieldsFromJson(json_string) {
    var fieldID = $('#programmeID')
    var fieldName = $('#programmeName')
    var fieldLevel =   $('#level')

    fieldID.attr('value', json_string["id"]);
    fieldName.attr('value', json_string["name"]);
    fieldLevel.attr('value', json_string["level"]);

}

function getProgrammeInfo(id) {
    $.ajax({
        type: "POST",
        url: "/api/programme",
        data: JSON.stringify({"id": id}),
        contentType: "application/json",
        dataType: 'json',
        success: function (text) {
            updateFieldsFromJson(text);
        }
    });
}

dropdown = $('#selectedProgramme');

dropdown.change(function(event) {
    getProgrammeInfo(dropdown.val());
});
