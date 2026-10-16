# ePro Select — Wholesale Inquiry 页面

按手机端设计稿还原的询盘页面，表单直接提交到 Web3Forms，**不需要任何后端代码**。

## 文件

| 文件 | 说明 |
|---|---|
| `index.html` | 页面本体，样式和脚本都在里面，单文件可直接上传 |
| `qr.png`（可选） | 放到同目录会自动替换页脚的二维码占位框 |

## 三步上线

### 1. 拿一个免费的 access key
打开 https://web3forms.com ，用你要接收询盘的邮箱（例如 `john@epro.com.cn`）验证，页面会给一串 access key。

### 2. 填进页面
打开 `index.html`，搜索 `ACCESS_KEY`，把这一行：

```js
var ACCESS_KEY = "YOUR_ACCESS_KEY_HERE";
```

换成：

```js
var ACCESS_KEY = "你拿到的那串key";
```

改完之后，页面顶部那条黄色的「尚未填入 access_key」提示会自动消失。

### 3. 上传
把 `index.html` 传到你的网站目录（或任意静态托管：Netlify / Vercel / GitHub Pages / 阿里云 OSS 都行），访问即可。

## 提交之后会发生什么

- 你填 key 时用的邮箱会收到一封邮件，包含客户填的全部内容
- Web3Forms 后台也会留档（免费版保存 30 天），可在 web3forms.com 登录查看
- 页面不跳转，按钮旁直接弹出设计稿里的 `Submitted successfully`

**免费额度：250 条 / 月。** 超出后可换服务或升级。

## 已经做进去的细节

- 深色配色取色自设计稿：底色 `#33363C`、卡片/输入框 `#272A2F`、顶栏页脚 `#3F4146`、必填星号 `#EA3323`
- 移动端优先，桌面端自动切成多列（≥760px 两列，≥1040px 三列）
- 必填校验：姓名、邮箱、国家、公司、隐私政策勾选；邮箱做格式校验
- 蜜罐字段 `botcheck` 防机器人
- 提交中按钮禁用并显示 `Sending...`，失败会提示

## 我改动了设计稿的这几个地方（如要还原请改回去）

1. 第二个表的标题原本也是 `Minimum Order Quantity (MOQ)`，但内容是天数，改成了 **Lead Time**
2. 第三个表标题原本同样是 `Minimum Order Quantity (MOQ)`，内容只有 `To be added.`，改成了 **Customization & Packaging**
3. `Company Name` 和 `Estimated Order Quantity` 原本没有 placeholder，补了 `Please enter your company name` / `e.g. 2,000 pcs`

对应位置在 `index.html` 里都有注释标注。

## 需要你核对的信息

从设计稿 OCR 出来的内容，麻烦确认一遍：

- 品牌名 `ePro Select`、邮箱 `john@epro.com.cn` / `dan@epro.com.cn`
- 地址：`9 Yiji Digital Building, Longjing'ao Road / No.3 Bantian Street, Longgang District / Shenzhen, Guangdong, China`
- MOQ 数值：1,860 / 3,000 / 460 / 1,000 / 680 / 900
- 交期：40-46 days、45-60 days

## 一个建议

设计稿里按钮是 `#B8B8B8` 浅灰底 + 近白色文字，对比度只有约 1.6:1，实际很难看清。想改的话，在 `index.html` 顶部把 `--btn-text:#E6E6E6` 改成 `--btn-text:#1C1E22` 即可。

## 待补

桌面端（1440）设计稿还没有拿到，目前桌面端是我按移动端的配色和栅格自己排的。导出 PNG 给我后可以对齐细节。
