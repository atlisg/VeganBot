angular.module('5fabApp', ['ngRoute']);

angular.module("5fabApp").controller("5fabController", function($scope, $http) {

	$scope.now = "";
	$scope.courses = [];

	$http.get('db.json').then(function(res) {
		$scope.courses = res.data;
	});

	$http.get('now.json').then(function(res) {
		$scope.now = res.data;
	});

});