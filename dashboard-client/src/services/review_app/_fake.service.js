import http from "./http.service";
import { createAxiosMocking } from '@/utils/mock.axios'

export default function () {

    const mocking = createAxiosMocking(http);

    mocking.addMock(/\/api\/token/i, () => {
        return {
            data: {
                access: 'The access Token',
                user: {
                    username: 'Mocked User',
                    is_superuser: false
                }
            }
        }
    })

    return mocking;
}