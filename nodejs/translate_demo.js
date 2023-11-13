const axios = require('axios');
const crypto = require('crypto');

const URL_SERVER = 'https://translate_dev.abcpen.com';
// const URL_SERVER = 'http://127.0.0.1:3701';
// const URL_SERVER = 'http://192.168.10.2:3701';
// const URL_SERVER = 'https://translate_v2.abcpen.com';

const text_zh = [
    '这粒稻，只是中国大粮仓丰收图景中的沧海一“稻”。黑龙江是中国产粮第一大省，去年粮食产量1573.5亿斤，占全国粮食总产量的11.5%，连续12年位居全国第一',
    '律回春辉渐，万象始更新。放眼神州大地，处处焕发文化新气象',
    '2023年11月5日至10日，第六届中国国际进口博览会将在上海举办。习近平主席在首届中国国际进口博览会开幕式主旨演讲中表示，中国对外开放的大门不会关闭，只会越开越大。作为世界上第一个以进口为主题的国家级展会，现在，进博会已成为中国构建新发展格局的窗口、推动高水平开放的平台、全球共享的国际公共产品，也是“一带一路”建设的重要支撑。我们一起来重温习近平主席的重要讲话！',
];

const sentences_zh = `
    首先，ASML作为全球最大的光刻机制造厂商，尽管能够领跑全世界，可如果没有大批金主客户，ASML也不会过得那么舒坦。中国市场作为全球最大的消费市场，
    在近年来，国内的半导体企业数量飙升，全球每新增20家半导体企业，就有19家是中国的，可见中国市场的巨大潜力。ASML也不傻，虽然在之前一直未大量出口给中国光刻机，但是随着中国对DUV光刻机需求的增长，ASML也开始重视起中国市场了。
`;

const application_key = 'test1';
const application_secret = '2258ACC4-199B-4DCB-B6F3-C2485C63E85A';

function generateSignature(appId, apiKey) {
    const ts = Math.floor(new Date().getTime() / 1000).toString();
    const baseString = crypto
        .createHash('md5')
        .update(appId + ts)
        .digest('hex');
    const apiKeyBuffer = Buffer.from(apiKey, 'utf-8');
    const signa = crypto.createHmac('sha1', apiKeyBuffer).update(baseString).digest('base64');
    return [signa, ts];
}

async function translateSentence(sentence, sourceLang, targetLang) {
    const [expectedSignature, timestamp] = generateSignature(application_key, application_secret);

    const headers = {
        'X-App-Key': application_key,
        'X-App-Signature': expectedSignature,
        'X-Timestamp': timestamp,
    };

    const values = {
        sentence: Buffer.from(sentence, 'utf-8').toString('base64'),
        source_lang: sourceLang,
        target_lang: targetLang,
    };

    try {
        const response = await axios.post(`${URL_SERVER}/v1/translate/sentence`, values, { headers });
        console.log(`translateSentence, Result: ${JSON.stringify(response.data)}`);
    } catch (error) {
        console.error(`translateSentence error: ${error.message}`);
    }
}

async function translateSentences(sentences, sourceLang, targetLang) {
    const [expectedSignature, timestamp] = generateSignature(application_key, application_secret);

    const headers = {
        'X-App-Key': application_key,
        'X-App-Signature': expectedSignature,
        'X-Timestamp': timestamp,
    };

    const values = {
        sentences: sentences,
        source_lang: sourceLang,
        target_lang: targetLang,
    };

    try {
        const response = await axios.post(`${URL_SERVER}/v1/translate/sentences`, values, { headers });
        console.log(`translateSentences, Result: ${JSON.stringify(response.data)}`);
    } catch (error) {
        console.error(`translateSentences error: ${error.message}`);
    }
}

async function translateFile(file, sourceLang, targetLang) {
    const [expectedSignature, timestamp] = generateSignature(application_key, application_secret);

    const headers = {
        'X-App-Key': application_key,
        'X-App-Signature': expectedSignature,
        'X-Timestamp': timestamp,
    };

    const formData = new FormData();
    formData.append('document', fs.createReadStream(`./${file}`));
    formData.append('target_lang', targetLang);

    try {
        const response = await axios.post(`${URL_SERVER}/v1/translate/file`, formData, { headers });
        console.log(`translateFile, Result: ${JSON.stringify(response.data)}`);
    } catch (error) {
        console.error(`translateFile error: ${error.message}`);
    }
}

async function translateDetection(sentences) {
    const [expectedSignature, timestamp] = generateSignature(application_key, application_secret);

    const headers = {
        'X-App-Key': application_key,
        'X-App-Signature': expectedSignature,
        'X-Timestamp': timestamp,
    };

    const values = { text: sentences };

    try {
        const response = await axios.post(`${URL_SERVER}/v1/translate/language_detection`, values, { headers });
        console.log(`translateDetection, Result: ${JSON.stringify(response.data)}`);
    } catch (error) {
        console.error(`translateDetection error: ${error.message}`);
    }

    for (const text of sentences) {
        try {
            const response = await axios.get(`${URL_SERVER}/v1/translate/language_detection?text=${encodeURIComponent(text)}`, { headers });
            console.log(`${text}, language detect result==> ${JSON.stringify(response.data)}`);
        } catch (error) {
            console.error(`Language detection error: ${error.message}`);
        }
    }
}

async function totalTest() {
    await translateSentence(sentences_zh, 'zh', 'ru');
    console.log('\n\n');
    await translateSentences(text_zh, 'zh', 'ru');
    console.log('\n\n');
    await translateFile('news_1.txt', 'zh', 'ru');
    console.log('\n\n');
    await translateDetection(multi_sentences);
    console.log('\n\n');
}

async function totalSentence() {
    for (const item of text_zh) {
        await translateSentence(item, 'zh', 'en');
    }
}

(async () => {
    const t1 = Date.now();
    for (let i = 0; i < 1; i++) {
        await totalTest();
        await totalSentence();
        await translateFile('news_1.txt', 'zh', 'ru');
    }
    const t2 = Date.now();
    console.log(`Total time: ${(t2 - t1) / 1000}s`);
})();
