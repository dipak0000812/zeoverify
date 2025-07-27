const express = require('express');
const router = express.Router();
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
const { verifyDocument } = require('../controllers/verifyController');

router.post('/', upload.single('file'), verifyDocument);

module.exports = router;
