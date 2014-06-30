'use strict';

/* Controllers */

angular.module('myApp.controllers', [])
  .controller('CalendarCtrl', ['$scope', function($scope) {

  }])
  .controller('StudentListCtrl', ['$scope', function($scope) {
  	$scope.students = [
    {'name': 'Alex Kyllo',
     'url': '/users/1/'},
    {'name': 'Dawn Xu',
     'url': '/users/2/'}
  	];
  }]);
