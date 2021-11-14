function updateAssessmentFields(json_string) {
    var fieldAssessmentNumber = $('#assessmentNumber');
    var fieldAssessmentName = $('#assessmentName');
    var fieldMaximumMark = $('#maximumMark');
    var fieldCourseName = $('#courseName')

    fieldAssessmentNumber.attr('value', json_string["number"]);
    fieldAssessmentName.attr('value', json_string["name"]);
    fieldMaximumMark.attr('value', json_string["maximumMark"]);
    fieldCourseName.attr('value', json_string["course_name"])

}

function getAssessmentInfo(id) {
    $.ajax({
        type: "POST",
        url: "/api/assessment",
        data: JSON.stringify({"id": id, "get_course_name": true}),
        contentType: "application/json",
        dataType: 'json',
        success: function (text) {
            updateAssessmentFields(text);
        }
    });
}

assessmentDropdown = $('#selectedAssessment');

assessmentDropdown.change(function(event) {
    getAssessmentInfo(assessmentDropdown.val());
});
