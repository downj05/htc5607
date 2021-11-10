function updateFieldsFromJson(json_string) {
    var fieldCourseID = $('#courseID');
    var fieldCourseName = $('#courseName');
    var fieldCredits = $('#credits');

    var fieldStatusCurrent = $('#current');
    var fieldStatusSuspended = $('#suspended');

    fieldCourseID.attr('value', json_string["id"]);
    fieldCourseName.attr('value', json_string["name"]);
    fieldCredits.attr('value', json_string["credits"]);

    if (json_string["status"] === 'current') {
        fieldStatusCurrent.prop('checked', true)
    } else {
        fieldStatusSuspended.prop('checked', true)
    }
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
