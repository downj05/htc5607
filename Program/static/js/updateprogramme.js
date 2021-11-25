function updateFieldsFromJson(json_string) {
    var fieldProgrammeID = $('#programmeID');
    var fieldProgrammeName = $('#programmeName');
    var fieldLevel = $('#level');


    fieldProgrammeID.attr('value', json_string["id"]);
    fieldProgrammeName.attr('value', json_string["name"]);
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

document.querySelector('#updateProgrammeForm').addEventListener("submit", function(e){
        if(!window.confirm("Are you sure you want to update the programme?")){
            e.preventDefault();    //stop form from submitting
        }
}); // confirmation box
