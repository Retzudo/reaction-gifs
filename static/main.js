(function() {
    "use strict";
    
    var app = angular.module('GifsApp', []);

    app.controller('GifsController', ['$scope', '$http', function($scope, $http) {
        $scope.gifs = [];
        $scope.search = '';

        $http.get('/gifs.json').then(function (response) {
            $scope.gifs = response.data.gifs;
        });
    }]);
})();
