var express = require('express');
var rpc_client = require('../rpc_client/rpc_client');
var router = express.Router();

/* GET news listing. */
router.get('/userId/:userId/pageNum/:pageNum', function(req, res, next) {
  console.log('Fetching news...');
  user_id = req.params['userId'];
  page_name = req.params['pageNum'];
  rpc_client.getNewsSummariesForUser(user_id, page_name, function(response){
      res.json(response);
  });
});

module.exports = router;
