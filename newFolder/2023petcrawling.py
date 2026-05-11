import asyncio
from playwright.async_api import async_playwright

async def pet():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.animal.go.kr/front/awtis/public/publicAllList.do")

        await page.locator('input[name="searchSDate"]').fill("2023-01-01")
        await page.locator('input[name="searchEDate"]').fill("2023-12-31")
        await page.locator('select[name="searchUprCd"]').select_option(label="서울특별시")
        await page.get_by_role("button", name="조회").click()
        
        await page.wait_for_selector('li:has-text("공고번호")', timeout=10000)

        results = []
        current_page = 1
        max_page = 222 

        while current_page <= max_page:
            print(f"\n{current_page} 페이지 수집 중")
            await page.wait_for_timeout(2000)
            pets = await page.query_selector_all('li:has-text("공고번호")')
            for pet in pets:
                status_tag = await pet.query_selector('.info-item:has-text("상태") .value')
                if status_tag:
                    status = (await status_tag.inner_text()).strip()
                    if "종료(반환)" in status:
                        breed_tag = await pet.query_selector('div.subject')
                        breed = (await breed_tag.inner_text()).strip() if breed_tag else "없음"
                        id_tag = await pet.query_selector(".info-item:has-text('공고번호') .value")
                        notice_id = (await id_tag.inner_text()).strip() if id_tag else "없음"
                        data = {"품종": breed, "상태": status, "공고번호": notice_id}
                        print(f"[수집] {data}")
                        results.append(data)
            current_page += 1
            if current_page > max_page: 
                break
            try:
                next_button = page.get_by_title("다음페이지").first
                if await next_button.is_visible():
                    await next_button.click()
                    await page.wait_for_load_state("networkidle")
                else:
                    print("페이지 버튼 없음")
                    break
            except Exception as e:
                print(f"오류 발생: {e}")
                break
        print(f"수집: {len(results)}건")
        await browser.close()
asyncio.run(pet())