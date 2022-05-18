export interface ApiException {
    error: any
    status: number
}

class Exceptions implements ApiException {
    constructor(readonly error: any, readonly status: number) {}
}

export class NotFoundException extends Exceptions {
    constructor(error: any) {
        super(error, 404)
    }
}

export class BadRequestException extends Exceptions {
    constructor(error: any) {
        super(error, 400)
    }
}
