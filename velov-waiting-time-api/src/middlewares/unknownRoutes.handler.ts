import {NotFoundException} from '~/utils/exceptions'

export const UnknownRoutesHandler = () => {
    throw new NotFoundException(`The requested resource does not exist`)
}
