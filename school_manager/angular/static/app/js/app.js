'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
  'myApp.filters',
  'myApp.services',
  'myApp.directives',
  'myApp.controllers',
  'ngResource',
  'ngCookies',
  'ui.bootstrap',
  'ui.calendar'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/calendar', {templateUrl: '../static/app/partials/calendar.html', controller: 'CalendarCtrl'});
  $routeProvider.when('/students', {templateUrl: '../static/app/partials/students.html', controller: 'StudentListCtrl'});
  $routeProvider.when('/courses', {templateUrl: '../static/app/partials/courses.html', controller: 'CourseListCtrl'});
  $routeProvider.otherwise({redirectTo: '/'});
}]).
config(['$httpProvider', function($httpProvider){
  // django and angular both support csrf tokens. This tells
  // angular which cookie to add to what header.
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
