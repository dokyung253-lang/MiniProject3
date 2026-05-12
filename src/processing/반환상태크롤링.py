import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def pet():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        await page.goto("https://www.animal.go.kr/front/awtis/public/publicAllList.do")

        await page.locator('input[name="searchSDate"]').fill("2023-01-01")
        await page.locator('input[name="searchEDate"]').fill("2024-12-31")
        await page.locator('select[name="searchUprCd"]').select_option(label="서울특별시")
        
        await page.get_by_role("button", name="조회").click()
        await page.wait_for_load_state("networkidle")
        
        await page.wait_for_selector('li:has-text("공고번호")', timeout=15000)

        results = []
        visited_ids = set() 
        current_page = 1
        max_page = 710 

        while current_page <= max_page:
            raw_text = await page.locator('li.active').inner_text()
            clean_page_num = "".join(filter(str.isdigit, raw_text))
            print(f"\n[{clean_page_num} 페이지 수집 중]")
            
            await page.wait_for_timeout(1000) 
            pets = await page.query_selector_all('li:has-text("공고번호")')
            
            for pet in pets:
                status_tag = await pet.query_selector('.info-item:has-text("상태") .value')
                if status_tag:
                    status = (await status_tag.inner_text()).strip()
                    
                    # 상태=종료(반환)
                    if "종료(반환)" in status:
        
                        # 공고 번호
                        id_tag = await pet.query_selector(".info-item:has-text('공고번호') .value")
                        notice_id = (await id_tag.inner_text()).strip() if id_tag else "없음"

                        # 중복 여부 판단
                        if notice_id in visited_ids or notice_id == "없음":
                            continue

                        # 등록 번호
                        reg_id_tag = await pet.query_selector(".info-item:has-text('등록번호') .value")
                        reg_id = (await reg_id_tag.inner_text()).strip() if reg_id_tag else "없음"
                        
                        data = {"상태": status, "공고번호": notice_id, "등록번호": reg_id}
                        print(f" [수집] {data}")
                        
                        results.append(data)
                        visited_ids.add(notice_id)

            # 페이지 이동
            try:
                next_num_link = page.locator('li.active + li:not(.next):not(.prev) a')
                
                if await next_num_link.count() > 0 and await next_num_link.is_visible():
                    await next_num_link.click()
                else:
                    next_block_button = page.locator('li.next a[title="다음페이지로"]').first
                    if await next_block_button.is_visible():
                        await next_block_button.click()
                    else:
                        print("더 이상 이동할 페이지가 없습니다.")
                        break
                
                current_page += 1
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_timeout(800)

            except Exception as e:
                print(f"페이지 이동 중 오류 발생: {e}")
                break

        # 결과
        with_reg = [d for d in results if d['등록번호'].strip() != ""]
        without_reg = [d for d in results if d['등록번호'].strip() == ""]
        print(f"[전체 수집 데이터]: {len(results)}건")
        print(f"[등록번호가 있는 거] : {len(with_reg)}건")
        print(f"[등록번호가 없는 거] : {len(without_reg)}건")

        df = pd.DataFrame(results)
        df.to_csv('./src/processing/반환상태크롤링.csv', 
                  index=False, 
                  encoding='utf-8',
                  na_rep='Unknown', 
                  header=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(pet())