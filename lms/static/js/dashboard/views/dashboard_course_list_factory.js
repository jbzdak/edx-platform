;(function (define) {
    'use strict';

    define(['backbone', 'js/dashboard/views/course_list_tabbed_view'],
        function (Backbone, CourseListTabbedView) {

            return function () {

                var courseListTabbedView = new CourseListTabbedView();
                courseListTabbedView.render();
            };
        });

}).call(this, define || RequireJS.define);
