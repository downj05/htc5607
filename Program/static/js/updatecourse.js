function updateFieldsFromJson(json_string) {
    var fieldCourseID = $('#courseID');
    var fieldCourseName = $('#courseName');
    var fieldCredits = $('#credits');
    var fieldFee = $('#fee');

    var fieldStatusCurrent = $('#current');
    var fieldStatusSuspended = $('#suspended');

    var fieldProgramme = $('#programmeName');


    fieldCourseID.attr('value', json_string["id"]);
    fieldCourseName.attr('value', json_string["name"]);
    fieldCredits.attr('value', json_string["credits"]);
    fieldFee.attr('value', json_string["fee"]);

    if (json_string["status"] === 'current') {
        fieldStatusCurrent.prop('checked', true)
    } else {
        fieldStatusSuspended.prop('checked', true)
    }

    $.ajax({
        type: "POST",
        url: "/api/programme",
        data: JSON.stringify({"id": json_string["programmeID"]}),
        contentType: "application/json",
        dataType: 'json',
        success: function (json_string) {
            fieldProgramme.attr('value', json_string["name"]);
        }
    });

}

function getCourseInfo(id) {

    $.ajax({
        type: "POST",
        url: "/api/course",
        data: JSON.stringify({"id": id}),
        contentType: "application/json",
        dataType: 'json',
        success: function (text) {
            updateFieldsFromJson(text);
        }
    });
}

dropdown = $('#selectedCourse');

dropdown.change(function(event) {
    getCourseInfo(dropdown.val());
});

document.querySelector('#updateCourseForm').addEventListener("submit", function(e){
        if(!window.confirm("Are you sure you want to update the course?")){
            e.preventDefault();    //stop form from submitting
        }
}); // confirmation box