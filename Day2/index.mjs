
import {
  S3Client,
  GetObjectCommand,
  PutObjectCommand,
} from "@aws-sdk/client-s3";
import sharp from "sharp";

const S3 = new S3Client();
// Lấy tên bucket đích
const DEST_BUCKET = process.env.DEST_BUCKET;
const THUMBNAIL_WIDTH = 200; // px
const SUPPORTED_FORMATS = {
  jpg: true,
  jpeg: true,
  png: true,
};

export const handler = async (event, context) => {
  const { eventTime, s3 } = event.Records[0];
  const srcBucket = s3.bucket.name;

  const srcKey = decodeURIComponent(s3.object.key.replace(/\+/g, " "));
  const ext = srcKey.replace(/^.*\./, "").toLowerCase();

  // Log thông tin sự kiện
  console.log(`${eventTime} - ${srcBucket}/${srcKey}`);

  // Kiểm tra định dạng file có được hỗ trợ không
  if (!SUPPORTED_FORMATS[ext]) {
    console.log(`ERROR: Unsupported file type (${ext})`);
    return;
  }

  try {
    // Lấy file từ bucket nguồn
    const { Body, ContentType } = await S3.send(
      new GetObjectCommand({
        Bucket: srcBucket,
        Key: srcKey,
      })
    );
    // Chuyển đổi Body sang dạng byte array để xử lý
    const image = await Body.transformToByteArray();
    // Resize ảnh sử dụng thư viện sharp
    const outputBuffer = await sharp(image).resize(THUMBNAIL_WIDTH).toBuffer();

    // Lưu ảnh đã resize vào bucket đích
    await S3.send(
      new PutObjectCommand({
        Bucket: DEST_BUCKET,
        Key: srcKey,
        Body: outputBuffer,
        ContentType,
      })
    );
    // Log thông báo thành công
    const message = `Successfully resized ${srcBucket}/${srcKey} and uploaded to ${DEST_BUCKET}/${srcKey}`;
    console.log(message);
    return {
      statusCode: 200,
      body: message,
    };
  } catch (error) {
    console.log(error);
  }
};